import os
from collections import OrderedDict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Union

import aiohttp
import requests
from aiohttp import ClientSession


class RequestType(Enum):
    GET = "GET"
    POST = "POST"


class Api(object):
    DEFAULT_API_KEY_DIR: str = os.path.expanduser("~/.knapsack_local/api_keys")

    def __init__(self) -> None:
        self.base_url = self._init_base_url()
        self.org_names_to_api_keys = {}
        self.org_names_to_api_keys, self.org_names_to_key_filenames = self._init_api_keys()

    def _init_base_url(self) -> str:
        base_url = os.environ.get("KNAPSACK_API_BASE_URL", None)
        if base_url:
            return base_url
        return "https://knap.ai"

    def _init_api_keys(self) -> Union[OrderedDict, OrderedDict]:
        filenames_to_api_keys = self._get_api_keys()
        api_keys = list(filenames_to_api_keys.values())
        response = self.GET(
            endpoint="org_names", org_name="",
            info={"api_keys": api_keys}
        )
        org_names = response.json()['orgNames']

        org_names_to_api_keys = OrderedDict()
        org_names_to_key_filenames = OrderedDict()
        if org_names is None or len(org_names) <= 0:
            return OrderedDict(), OrderedDict()
        for i, org_name in enumerate(org_names):
            key_filename, api_key = list(filenames_to_api_keys.items())[i]
            org_names_to_api_keys[org_name] = api_key
            org_names_to_key_filenames[org_name] = key_filename
        return org_names_to_api_keys, org_names_to_key_filenames

    def _get_api_keys(self) -> OrderedDict:
        api_key_dir = os.environ.get('KNAPSACK_API_KEY_DIR')
        if api_key_dir is not None:
            env_api_key_dir = Path(os.environ.get('KNAPSACK_API_KEY_DIR'))
            if env_api_key_dir.exists():
                return self._read_api_keys_from_dir(env_api_key_dir)
        elif Path(self.DEFAULT_API_KEY_DIR).exists():
            return self._read_api_keys_from_dir(self.DEFAULT_API_KEY_DIR)
        else:
            raise ValueError(
                "No API keys found in either env var KNAPSACK_API_KEY_DIR " +
                "or in ~/.knapsack_local/api_keys. Make sure that your API " +
                "key ends with \".key\"."
            )

    def _read_api_keys_from_dir(self, dir_path: Path) -> OrderedDict:
        key_filenames = os.listdir(str(dir_path))
        filenames_to_api_keys = OrderedDict()
        for key_filename in key_filenames:
            key_file = dir_path / Path(key_filename)
            if key_file.suffix == ".key":
                with open(key_file, 'r') as f:
                    api_key = f.readline()
                    api_key = api_key.strip()
                    filenames_to_api_keys[key_filename] = api_key
        return filenames_to_api_keys

    def get_base_url(self) -> str:
        return self.base_url

    def ls(self, info: Dict[str, Any] = {}):
        endpoint = "ls"
        api_keys = list(self.org_names_to_api_keys.values())
        info["api_keys"] = api_keys
        return requests.get(self.base_url + "/" + endpoint, json=info)

    def GET(
        self,
        endpoint: str,
        org_name: str,
        info: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        api_key = self.org_names_to_api_keys.get(org_name, "")
        if api_key != "":
            info["api_key"] = api_key
        result = requests.get(self.base_url + "/" + endpoint, json=info)
        return result

    def POST(
        self,
        endpoint: str,
        org_name: str,
        info: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        info["api_key"] = self.org_names_to_api_keys.get(org_name, "")
        result = requests.post(self.base_url + "/" + endpoint, json=info)
        return result

    async def async_request(
        self,
        session: ClientSession,
        method: RequestType,
        endpoint: str,
        info: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        info["api_key"] = self._load_api_key()
        try:
            result = await session(
                method=str(method),
                url=self.base_url + "/" + endpoint,
                json=info
            )
        except (
            aiohttp.ClientError,
            aiohttp.http_exceptions.HttpProcessingError,
        ) as e:
            print(f"Error sending async request: {e}")
            return None
        print(f"{method} result: ", result)
        return result
