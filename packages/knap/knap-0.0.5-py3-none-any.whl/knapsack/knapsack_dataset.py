import asyncio
import concurrent.futures
from os.path import expanduser
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

import tomllib
import tqdm.asyncio
from aiohttp import ClientSession

from knapsack.api import Api, RequestType
from knapsack.blueprints import Blueprints, Blueprint
from knapsack.kd_builder import KDBuilder
from knapsack.storage.base_store import BaseStore
from knapsack.storage.b2_store import B2Store
from knapsack.storage.fs_store import FSStore
from knapsack.split import Split
from knapsack.storage_provider import StorageProvider


class Operation(Enum):
    STORE = "STORE"
    APPEND = "APPEND"
    MERGE = "MERGE"
    PROCURE = "PROCURE"


KNAPSACK_CONFIG_FILE: Path = Path(expanduser("~/.knapsack.toml"))


class KnapsackDataset(object):
    knapsack_cfg: Dict[str, Any] = None
    name_to_remote_knapsack: Dict[str, BaseStore] = {}
    name_to_local_knapsack: Dict[str, BaseStore] = {}
    main_remote_knapsack: BaseStore = None
    default_local_knapsack: BaseStore = None

    MAX_WORKERS: int = 64

    def __init__(
        self,
        name: Optional[str] = None,
        org_name: Optional[str] = None,
        repro_tag: Optional[str] = None,
    ) -> None:
        if self.knapsack_cfg is None:
            KnapsackDataset.init_knapsack()

        self.current_local_knapsack = self.default_local_knapsack

        self.name = name
        self.org_name = org_name
        self.repro_tag = repro_tag
        self.total_bytes_used = 0

        self.api = Api()
        if self._is_well_defined_dataset(self.name, self.org_name, self.repro_tag):
            self.procure()
        else:
            raise ValueError("Either a name/org_name pair or a repro_tag must " +
                             "be given as arguments to KnapsackDataset.")

    @classmethod
    def init_knapsack(cls):
        with open(KNAPSACK_CONFIG_FILE, "rb") as f:
            cls.knapsack_conf = tomllib.load(f)

        remote_knapsack_configs = cls.knapsack_conf['knapsack']['remote']
        if len(remote_knapsack_configs) <= 0:
            raise ValueError(".knapsack.toml did not contain any remote knapsacks.")

        main: str = None
        for ks in remote_knapsack_configs:
            if ks['path'] == 'KNAP_CLOUD':
                store = B2Store(name=ks['name'])
            else:
                store = FSStore(name=ks['name'], is_local=False)
            cls.name_to_remote_knapsack[ks['name']] = store

            if 'tag' in ks and ks['tag'] == 'main':
                main = ks['name']
                cls.main_remote_knapsack = store

        if main is None:
            raise ValueError("Did not find a remote knapsack with tag 'main'.")

        local_knapsack_configs = cls.knapsack_conf['knapsack']['local']
        if len(local_knapsack_configs) <= 0:
            raise ValueError(".knapsack.toml did not contain any local knapsacks.")

        for ks in local_knapsack_configs:
            store = FSStore(name=ks['name'], is_local=True)
            cls.name_to_local_knapsack[ks['name']] = store
            if 'tag' in ks and ks['tag'] == 'default':
                default = ks['name']
                cls.default_local_knapsack = store

        if default is None:
            raise ValueError("Did not find a local knapsack with tag 'default'.")

    def __del__(self):
        # TODO: I'm pretty sure this needs to delete the DP index
        # metadata/Local Knapsack record in the case where the dataset
        # is never stored, appended, etc. because the Local Knapsack
        # dataset could end up out of sync with the Remote? Idk. Need
        # to think more about that case.
        pass

    def _is_well_defined_dataset(
        self,
        name: str,
        org_name: str,
        repro_tag: str
    ) -> bool:
        if (self.repro_tag is not None or (self.name is not None and
                                           self.org_name is not None)):
            return True
        return False

    def from_kd_builder(
        self,
        kd_builder: KDBuilder,
        local_knapsack_name: str = None,
    ) -> None:
        if local_knapsack_name is not None:
            self.current_local_knapsack = self.name_to_local_knapsack[name]

        # TODO: maybe we can do away with this method somehow. It's currently
        # used for .store() but not .append(), which is a little awkward.
        self.kd_builder = kd_builder

    def set_dataset_by_repro_tag(self, repro_tag: str) -> None:
        # TODO: this should probably set both self.name
        # and self.org_name
        self.repro_tag = repro_tag
        self._is_well_defined_dataset(None, None, self.repro_tag)

    def set_dataset_by_name(self, name: str, org_name: str) -> None:
        # TODO: this function should probably set self.repro_tag as well
        self.name = name
        self.org_name = org_name
        self._is_well_defined_dataset(self.name, self.org_name)

    async def _transfer_all_files(
        self,
        src: FSStore,
        dst: FSStore,
        blueprint: Blueprint,
        cloud_provider_info: Dict[str, Any],
    ):
        executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.MAX_WORKERS,
        )
        loop = asyncio.get_event_loop()
        async with ClientSession() as session:
            tasks = []
            for file in src.iterate_over_files(self.org_name, self.name, blueprint):
                tasks.append(loop.run_in_executor(
                    executor,
                    self._transfer_file,
                    src,
                    dst,
                    Path(file),
                    blueprint.get_bucket_url(),
                ))
            src_blueprints = src.read_blueprints(
                self.org_name, self.name,
            )
            tasks.append(dst.update_blueprints(
                src_blueprints, self.org_name, self.name,
            ))
            for task in tqdm.asyncio.tqdm.as_completed(tasks):
                await task

    def _transfer_file(
        self,
        src: BaseStore,
        dst: BaseStore,
        full_src_file_path: Path,
        bucket_url: str,
    ) -> int:
        """
        Returns number of size of file in bytes.
        """
        # TODO: Recording of bytes transferred needs to be more
        # robust.
        # UPDATE: turns out the API calls to Backblaze to check
        # storage used are cheaper than I thought.
        # Can probably use those.
        filename = Path(full_src_file_path.name)
        if isinstance(src, B2Store) and isinstance(dst, FSStore):
            data = b""
            # TODO: converting remote url to local only works here because B2Store is always used remote.
            storage_url = dst.convert_remote_url_to_local(bucket_url)

            local_file_path = dst.root / storage_url / filename
            if not dst._file_exists(local_file_path):
                src.download_file(
                    b2_file_path=full_src_file_path,
                    local_bucket_path=local_file_path
                )
        elif isinstance(dst, B2Store):
            data = src.read_bytes_from_file(full_src_file_path)
            dst.upload_file(
                src_file_path=full_src_file_path,
                b2_file_path=dst.root / Path(bucket_url) / filename
            )
        else:
            data = src.read_bytes_from_file(full_src_file_path)
            dst.store_file(
                src_file=full_src_file_path,
                bucket_url=bucket_url,
                filename=filename,
            )
        self.total_bytes_used += len(data)

    def _init_op(
        self,
        op: Operation,
        data: Union[KDBuilder, Any],
        data_store: BaseStore,
    ):
        if op == Operation.STORE:
            result = self.api.POST(
                endpoint="store/init",
                org_name=self.org_name,
                info={
                    'dataset_name': self.name,
                    'storage_provider': data_store.who_am_i(),
                    'num_data_points': data.get_total_num_data_points(),
                }
            )
        elif op == Operation.APPEND:
            result = self.api.POST(
                endpoint="append/init",
                org_name=self.org_name,
                info={
                    'dataset_name': self.name,
                    'storage_provider': data_store.who_am_i(),
                    'num_data_points': data.get_total_num_data_points(),
                    'original_repro_tag': self.repro_tag,
                }
            )
        elif op == Operation.PROCURE:
            result = self.api.GET(
                "procure",
                org_name=self.org_name,
                info={
                    "repro_tag": self.repro_tag,
                    "org_name": self.org_name,
                    "name": self.name,
                    'storage_provider': data_store.who_am_i(),
                }
            )
        return result

    def _close_op(
        self,
        op: Operation,
        transaction_id: int,
        repro_tag: str,
        blueprints: Blueprints,
        bytes_used: int,
    ):
        info = {
            'transaction_id': transaction_id,
            'repro_tag': self.repro_tag,
            'dataset_name': self.name,
            'bytes_used': str(bytes_used),
        }
        if op == Operation.STORE:
            result = self.api.POST(
                endpoint="store/close",
                org_name=self.org_name,
                info=info
            )
        elif op == Operation.APPEND:
            result = self.api.POST(
                endpoint="append/close",
                org_name=self.org_name,
                info=info
            )
            if 'blueprints' in result.json():
                blueprints = Blueprints.from_json(result.json())
                self.current_local_knapsack.update_blueprints(
                    blueprints, self.org_name, self.name,
                )

        elif op == Operation.PROCURE:
            return None

        return result

    def _launch_asyncio(self, fn: Callable):
        """
        This is a workaround for Jupyter Lab's issue with asyncio.
        It would be great to not need this function.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            loop = None

        if loop and loop.is_running():
            task = loop.create_task(fn)
            asyncio.wait_for(task)
            result = task.result()
        else:
            result = asyncio.run(fn)
        return result

    def _run_op(
        self,
        op: Operation,
        data: Union[KDBuilder, Any],
        remote_knapsack_name: str,
    ) -> str:
        """
        data should be either a KDBuilder
        or a KnapsackDataset
        """
        remote_knapsack = self.main_remote_knapsack
        if remote_knapsack_name is not None:
            remote_knapsack = self.name_to_remote_knapsack[name]

        response = self._init_op(op, data, remote_knapsack)

        response_json = response.json()
        transaction_id = response_json.get("transactionId", None)

        if 'blueprints' in response_json:
            blueprints = Blueprints.from_json(response_json)
        else:
            blueprints = Blueprints([])

        cloud_provider_info = response_json.get("cloudStorageApi", None)

        new_repro_tag = response_json.get("reproTag", None)

        for blueprint in blueprints:
            remote_knapsack.record_remote_prefixes(blueprint.get_bucket_url())

            if op == Operation.STORE or op == Operation.APPEND:
                remote_knapsack.prep_for_store(
                    self.org_name, self.name, blueprint.get_repro_tag(), cloud_provider_info
                )
                self._launch_asyncio(self._convert_to_local_knapsack(blueprint, kd_builder=data))
                self._launch_asyncio(self._transfer_all_files(
                    src=self.current_local_knapsack,
                    dst=remote_knapsack,
                    blueprint=blueprint,
                    cloud_provider_info=cloud_provider_info
                ))
            elif op == Operation.PROCURE:
                self.current_local_knapsack.prep_for_store(
                    self.org_name, self.name, blueprint.get_repro_tag(), cloud_provider_info
                )
                remote_knapsack.prep_for_store(
                    self.org_name, self.name, blueprint.get_repro_tag(), cloud_provider_info
                )

                self._launch_asyncio(self._transfer_all_files(
                    src=remote_knapsack,
                    dst=self.current_local_knapsack,
                    blueprint=blueprint,
                    cloud_provider_info=cloud_provider_info
                ))

        response = self._close_op(
            op, transaction_id, new_repro_tag, blueprints, bytes_used=self.total_bytes_used,
        )
        self.total_bytes_used = 0
        # if response is not None:
            # blueprints = Blueprints.from_json(response.json())
            # if blueprints is not None:
            #     self.current_local_knapsack.update_blueprints(
            #         blueprints, self.org_name, self.name
            #     )
            #     self.main_remote_knapsack.update_blueprints(
            #         blueprints, self.org_name, self.name
            #     )

        return new_repro_tag

    def store(self, dst_knapsack_name: str = None):
        """
        Stores dataset in Knapsack, loaded from a KDBuilder.

        If 'dst_knapsack_name' is set, use this knapsack as the place
        to store the data.
        """
        self.repro_tag = self._run_op(Operation.STORE, self.kd_builder, dst_knapsack_name)
        self.kd_builder = None
        return self.repro_tag

    async def _merge_request(
        self,
        repro_tag2: str,
        use_existing_dataset_name: bool
    ) -> str:
        async with ClientSession() as session:
            new_repro_tag = await self.api.async_request(
                session,
                RequestType.POST,
                endpoint="/merge",
                info={
                    "repro_tag1": self.repro_tag,
                    "repro_tag2": repro_tag2,
                    "use_first_dataset_name": use_existing_dataset_name,
                })
        return new_repro_tag

    def merge(
        self,
        new_data: Union[str, KDBuilder, Any],
        use_existing_dataset_name: bool
    ):
        """
        new_data should be either a repro_tag,
        KDBuilder, or KnapsackDataset.
        """
        if new_data is None:
            raise ValueError("Either a new KnapsackDataset or a" +
                             " KDBuilder must be passed to append.")
        if isinstance(new_data, str):
            second_repro_tag = new_data
        elif isinstance(new_data, KnapsackDataset):
            second_repro_tag = new_data.repro_tag
        elif isinstance(new_data, KDBuilder):
            second_repro_tag = self._run_op(Operation.STORE, new_data)

        self.repro_tag = self._launch_asyncio(self._merge_request(
            second_repro_tag, use_existing_dataset_name
        ))

    def append(
        self,
        new_data: KDBuilder,
        dst_knapsack_name: str = None,
    ):
        """
        new_data should be in the form of a KDBuilder.

        If 'dst_knapsack_name' is set, use this knapsack as the place
        to store the data.
        """
        if new_data is None:
            raise ValueError("Either a new KnapsackDataset or a" +
                             " KDBuilder must be passed to append.")
        self.repro_tag = self._run_op(Operation.APPEND, new_data, dst_knapsack_name)

    def procure(
        self,
        repro_tag: Optional[str] = None,
        dst_knapsack_name: str = None,
    ) -> None:
        """
        Procures dataset from Knapsack.

        Either the reproducibility tag needs to be passed,
        or the KnapsackDataset must have sufficient metadata
        to identify the dataset (name and org_name).

        If 'dst_knapsack_name' is set, use this knapsack as the place
        to fetch the data from.

        TODO: It would be great to have the option to store the
        data locally in different ways. What if someone wants the
        whole dataset in one folder to check it all at once,
        instead of having the lineage repro tags essentially
        housing the diffs from one to the next?
        """
        # TODO: would be nice if the user could check a different
        # method to make sure that procure (or any other Op) completed.
        # I'm imagining the case where a user wants to start a training
        # run after procuring data, but is not sure if the procure
        # finished (as that could screw up training, depending on their
        # implementation).
        if self.org_name is None:
            raise ValueError("No org_name supplied.")
        self.repro_tag = self._run_op(Operation.PROCURE, None, dst_knapsack_name)

    def __add__(self, d):
        """
        Shortcut for merge or append, depending on
        the data type of the second data object.
        d should be either a repro_tag,
        KDBuilder, or KnapsackDataset.
        """
        # TODO: Decide: should this always append?
        # If it merges, how does __add__ decide
        # what the dataset name is? Maybe if we can
        # set name retroactively, this could still
        # perform merges.
        if isinstance(d, KnapsackDataset):
            self.merge(d.repro_tag)
        elif isinstance(d, KDBuilder):
            self.append(d)
        else:
            raise ValueError("Cannot combine KnapsackDataset and %s" % type(d))

    async def _convert_to_local_knapsack(
        self,
        blueprint: Blueprint,
        kd_builder: KDBuilder
    ) -> None:
        executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.MAX_WORKERS,
        )
        loop = asyncio.get_event_loop()

        self.current_local_knapsack.prep_for_store(
            self.org_name, self.name, blueprint.get_repro_tag(), None
        )
        tasks = []
        idx = 0
        dp_idxs = blueprint.get_dp_indices()

        for i, dp_idx in enumerate(dp_idxs.iterate()):
            file = kd_builder[i]

            tasks.append(loop.run_in_executor(
                executor,
                self.current_local_knapsack.store_file,
                Path(file),
                self.org_name,
                Path(f"{dp_idx}"),
            ))
            dp_idxs.record_original_filename(
                file.name, idx
            )
            idx += 1
        tasks.append(self.current_local_knapsack.update_blueprints(
                new_data=blueprint,
                org_name=self.org_name,
                dataset_name=self.name
        ))
        await asyncio.gather(*tasks)

    def __len__(self) -> int:
        return self.get_total_num_data_points()

    def get_total_num_data_points(self) -> int:
        blueprints = self.current_local_knapsack.read_blueprints(self.org_name, self.name)
        blueprint = blueprints.get_blueprint(self.repro_tag)
        if blueprint is None:
            return 0
        return blueprint.get_num_data_points()

    def __str__(self) -> str:
        num_train = 0
        num_val = 0
        num_test = 0
        num_none = 0
        print(
            f"Dataset Name: {self.name} \n" +
            f"Repro Tag: {self.repro_tag} \n" +
            f"Num train samples: {num_train} \n" +
            f"Num val samples: {num_val} \n" +
            f"Num test samples: {num_test} \n" +
            f"Num samples of no split: {num_none} \n"
        )

    def __getitem__(self, i: int) -> Path:
        # TODO: optimize this function.
        if i >= len(self):
            i = i % len(self)
        blueprints = self.current_local_knapsack.read_blueprints(self.org_name, self.name)
        data_point_indices = blueprints.get_all_dp_indices_for_tag(self.repro_tag)
        data_point_idx = data_point_indices[i]
        return self.current_local_knapsack.get_data_by_idx(
            self.org_name, self.name, data_point_idx
        )
