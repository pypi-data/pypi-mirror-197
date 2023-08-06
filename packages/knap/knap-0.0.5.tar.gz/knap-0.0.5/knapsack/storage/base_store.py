import json
import os
import shutil
from abc import ABC, abstractmethod
from os import listdir
from pathlib import Path
from tqdm import tqdm
from typing import Any, Dict, List, Union

from knapsack.blueprints import Blueprints, Blueprint, DataPointIndices
from knapsack.split import Split


class BaseStore(ABC):
    KNAPSACK_LOCAL_STORAGE: str = os.path.expanduser(
        "~/.knapsack_local/storage"
    )
    KNAPSACK_REMOTE_STORAGE: str = os.path.expanduser(
        "~/.knapsack_remote/storage"
    )

    BLUEPRINTS_FILENAME: str = "blueprints.json"

    def __init__(
        self,
        name: str,
        is_local: bool = True,
    ) -> None:
        self.name = name
        self.org_name_to_prefix = {}
        self.is_local = is_local
        self.root = self._get_root()

    @abstractmethod
    def _get_root(self) -> Path:
        raise NotImplementedError("_get_root not implemented.")

    @abstractmethod
    def _file_exists(self, file_path: Path) -> bool:
        pass

    @abstractmethod
    def who_am_i(self) -> str:
        pass

    @abstractmethod
    def _write_file(self, file: bytes, path: Path) -> None:
        pass

    @abstractmethod
    async def _write_blueprints(self, blueprints: Blueprints, path: Path) -> None:
        pass

    # @abstractmethod
    def _mkdir(self, parents: bool) -> None:
        pass

    @abstractmethod
    def read_bytes_from_file(self, file: str) -> bytes:
        pass

    def _get_org_path(self, org_name: str) -> Path:
        org_prefix = self.org_name_to_prefix.get(org_name, "")
        full_org_path = Path(org_name)
        if org_prefix != "":
            full_org_path = Path(org_prefix, org_name)
        return full_org_path

    # def _get_dataset_path(self, dataset_name: str) -> Path:
    #     dataset_prefix = self.dataset_name_to_prefix.get(dataset_name, "")
    #     full_dataset_path = Path(dataset_name)
    #     if dataset_prefix != "":
    #         full_dataset_path = Path(dataset_prefix, dataset_name)
    #     return full_dataset_path

    def prep_for_store(
        self,
        org_name: str,
        dataset_name: str,
        repro_tag: str,
        cloud_provider_info: Dict[str, Any] = None,
    ) -> None:
        pass

    def convert_remote_url_to_local(self, storage_url: Path) -> Path:
        """
        storage_url should be of the format:
            <org_prefix>/<org_name>
        """
        # TODO: I really don't like having this codified here.
        components = str(storage_url).split("/")

        # org_prefix = components[0]
        org_name = components[1]
        # dataset_prefix = components[2]
        # dataset_name = components[3]
        return Path(org_name)  # / Path(dataset_name)

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
        # TODO: I really don't like having this codified here.
        components = storage_url.split("/")

        org_prefix = components[0]
        org_name = components[1]

        self.org_name_to_prefix[org_name] = org_prefix

    def _get_dataset_root(
        self,
        org_name: str,
        dataset_name: str,
    ) -> Path:
        """
        This function defines the location of an org's dataset within
        the local knapsack.
        """
        org_path = self._get_org_path(org_name)
        return self.root / org_path

    def iterate_over_files(
        self,
        org_name: str,
        dataset_name: str,
        blueprint: Blueprint
    ):
        data_dir = self._get_dataset_root(org_name, dataset_name)
        dp_indices = blueprint.get_dp_indices()
        for data_file_idx in tqdm(dp_indices.iterate()):
            yield Path(data_dir, str(data_file_idx))

    def get_data_by_idx(
        self,
        org_name: str,
        dataset_name: str,
        data_idx: int,
    ) -> Path:
        # TODO: may need to be generalized for multiple files per data point?
        data_dir = self._get_dataset_root(org_name, dataset_name)
        return data_dir / str(data_idx)

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

    def _get_blueprints_path(self, org_name: str, dataset_name: str) -> Path:
        return self._get_dataset_root(org_name, dataset_name) / \
            Path(self.BLUEPRINTS_FILENAME)

    def read_blueprints(
        self,
        org_name: str,
        dataset_name: str
    ) -> Blueprints:
        blueprints_path = self._get_blueprints_path(org_name, dataset_name)
        blueprints = Blueprints([])
        blueprints_bytes = self.read_bytes_from_file(blueprints_path)
        blueprints_str = blueprints_bytes.decode("utf-8")
        if len(blueprints_bytes) > 0:
            blueprints = json.loads(blueprints_bytes, object_hook=Blueprints.from_json)
        return blueprints

    async def update_blueprints(
        self,
        new_data: Union[Blueprint, Blueprints],
        org_name: str,
        dataset_name: str,
    ) -> None:
        existing_blueprints = self.read_blueprints(org_name, dataset_name)
        blueprints_path = self._get_blueprints_path(org_name, dataset_name)
        if isinstance(new_data, Blueprint):
            existing_blueprints.update(new_data)

        elif isinstance(new_data, Blueprints):
            for blueprint in new_data:
                existing_blueprints.update(blueprint)
        else:
            new_data_type = type(new_data)
            raise ValueError(f"update_blueprints only accepts a Blueprint. Got {new_data_type}")

        await self._write_blueprints(existing_blueprints, blueprints_path)
