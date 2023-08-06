import base64
import json
import os
import shutil
from os import listdir
from pathlib import Path
from typing import Any, Dict, List, Union

from knapsack.blueprints import Blueprint, Blueprints, DataPointIndices
from knapsack.split import Split
from knapsack.storage.base_store import BaseStore


class FSStore(BaseStore):
    def __init__(
        self,
        name: str,
        is_local: bool = True,
    ) -> None:
        super().__init__(name=name, is_local=is_local)
        self.org_name_to_prefix = {}
        self.is_local = is_local
        self._get_root()

    def _get_root(self) -> Path:
        if self.is_local:
            self.root = self._init_root()
        else:
            self.root = self._init_remote_root()

    def _init_root(self) -> Path:
        local_knapsack_dir = os.environ.get('KNAPSACK_LOCAL_STORAGE')
        if local_knapsack_dir is not None:
            local_knapsack_root = Path(local_knapsack_dir)
            if not local_knapsack_root.exists():
                local_knapsack_root.mkdir(parents=True, exist_ok=True)
            return local_knapsack_root
        local_knapsack_root = Path(self.KNAPSACK_LOCAL_STORAGE)
        local_knapsack_root.mkdir(parents=True, exist_ok=True)
        return local_knapsack_root

    def _init_remote_root(
        self,
    ) -> Path:
        remote_knapsack_dir = os.environ.get('KNAPSACK_REMOTE_STORAGE')
        if remote_knapsack_dir is not None:
            remote_knapsack = Path(remote_knapsack_dir)
        else:
            remote_knapsack = Path(self.KNAPSACK_REMOTE_STORAGE)
        if not remote_knapsack.exists():
            remote_knapsack.mkdir(parents=True, exist_ok=True)
        return remote_knapsack

    def _file_exists(self, file_path: Path) -> bool:
        return file_path.exists()

    def who_am_i(self) -> str:
        return "local"

    def _write_file(self, file: bytes, path: Path) -> None:
        with open(path, 'w') as f:

            json.dump(file, f)

    async def _write_blueprints(self, blueprints: Blueprints, path: Path) -> None:
        with open(path, 'w') as f:
            json.dump(blueprints.to_json(), f)

    def convert_remote_url_to_local(self, storage_url: Path) -> Path:
        """
        storage_url should be of the format:
            <org_prefix>/<org_name>
        """
        # TODO: I really don't like having this codified here.
        # Server should probably just return everything.
        components = str(storage_url).split("/")
        if len(components) != 2:
            return storage_url

        org_name = components[1]
        return Path(org_name)

    def am_i_local(self) -> bool:
        return self.is_local

    def record_remote_prefixes(
        self,
        storage_url: str,
    ):
        """
        storage_url should be of the format:
            <org_prefix>/<org_name>
        """
        # TODO: I really don't like having this structure codified here.
        components = storage_url.split("/")

        org_prefix = components[0]
        org_name = components[1]

        self.org_name_to_prefix[org_name] = org_prefix

    def prep_for_store(
        self,
        org_name: str,
        dataset_name: str,
        repro_tag: str,
        cloud_provider_info: Dict[str, Any] = None,
    ) -> None:
        org_path = self._get_org_path(org_name)
        for split in Split:
            dst_dir = Path(
                self.root, org_path
            )
            dst_dir.mkdir(parents=True, exist_ok=True)

    def store_file(
        self,
        src_file: Union[Path, bytes],
        bucket_url: str,
        filename: Path,
    ) -> None:
        """
        prep_for_store should be called first to prevent file not found
        errors in the case that any parent directories don't exist.
        """
        if self.am_i_local():
            bucket_url = self.convert_remote_url_to_local(Path(bucket_url))

        dst_file = self.root / bucket_url / filename
        if isinstance(src_file, Path):
            # This is essentially the "everything is local" function.
            # src_file is a Path when both local and remote are
            # FSStore.
            shutil.copy(str(src_file), str(dst_file))
        elif isinstance(src_file, bytes):
            # TODO: Maybe we can just always use this, instead of shutil.copy,
            # though perhaps there are performance gains with the above?
            with open(str(dst_file), 'wb') as f:
                f.write(src_file)

    def read_bytes_from_file(self, file: str) -> bytes:
        if Path(file).exists():
            with open(file, "rb") as f:
                return f.read()
        return b""

    def _get_matching_files(
        self,
        location: Path,
        dp_idxs: DataPointIndices
    ) -> List[Path]:
        """
        Return files in 'location' that are also in
        the datapoint indices.
        """
        if location.is_file():
            return [location]
        all_items = listdir(str(location))
        return [location / Path(f) for f in all_items]

    def split_iter(
        self,
        org_name: str,
        dataset_name: str,
        repro_tag: str,
        split: Split
    ):
        """
        Returns directories that house data points of this dataset.

        Iterate over a particular split.
        """
        split_dir = self._get_dataset_root(org_name, dataset_name) / \
            Path(repro_tag) / Path(str(split))
        if not split_dir.exists():
            yield None

        # split_data_points = split_dir.glob('**/*')
        # split_data_points = [x for x in split_data_points if x.is_file()]
        # for dp in split_data_points:
        #     yield dp
        yield split_dir
