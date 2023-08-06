import base64
import json
import os
from pathlib import Path
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

from knapsack.split import Split
from knapsack.storage.base_store import BaseStore
from knapsack.blueprints import Blueprint, Blueprints


class B2Store(BaseStore):
    def __init__(self, name: str):
        super().__init__(name=name, is_local=False)
        self.tmp_storage_dir = self.KNAPSACK_LOCAL_STORAGE

    def prep_for_store(
        self,
        org_name: str,
        dataset_name: str,
        repro_tag: str,
        cloud_provider_info: Dict[str, Any],
    ) -> None:
        rw_files_account = cloud_provider_info['capability_to_account']['files']
        self.bucket_name = rw_files_account['allowed']['bucketName']
        key_id = rw_files_account.get("applicationKeyId", None)
        key_value = rw_files_account.get("applicationKeyValue", None)

        self.api_url = rw_files_account.get("apiUrl", None)
        self.download_url = rw_files_account.get("downloadUrl", None)
        self.s3_api_url = rw_files_account.get("s3ApiUrl", None)

        self.b2 = self.get_b2_resource(self.s3_api_url, key_id, key_value)
        self.b2_client = self.get_b2_client(self.s3_api_url, key_id, key_value)

    def get_b2_resource(self, endpoint: str, key_id: str, application_key: str):
        b2 = boto3.resource(
            service_name='s3',
            endpoint_url=endpoint,
            aws_access_key_id=key_id,
            aws_secret_access_key=application_key,
            config=Config(
                signature_version='s3v4',
            )
        )
        return b2

    def get_b2_client(self, endpoint, keyID, applicationKey):
        b2_client = boto3.client(
            service_name='s3',
            endpoint_url=endpoint,
            aws_access_key_id=keyID,
            aws_secret_access_key=applicationKey
        )
        return b2_client

    def _get_root(self) -> Path:
        return Path("")

    def _file_exists(self, file_path: Path) -> bool:
        return False

    def who_am_i(self) -> str:
        return "b2"

    def _create_local_tmp_file(self, file_name: str) -> Path:
        return self.tmp_storage_dir / Path("tmp_" + file_name)

    def _mkdir(self, parents: bool) -> None:
        pass

    def read_bytes_from_file(self, file: Path) -> bytes:
        name = file.name

        dst_file_path = self.tmp_storage_dir / Path(f"tmp_{name}")
        self.download_file(file, dst_file_path)
        if not Path(dst_file_path).exists():
            return b""
        with open(dst_file_path, "rb") as f:
            file_bytes = f.read()
        # TODO: Reading files like this could make egress
        # fees less than transparent. How can we alleviate this?
        os.remove(str(dst_file_path))
        return file_bytes

    async def _write_file(self, file: bytes, path: Path) -> None:
        # TODO: would be great to cache things, like blueprints,
        # that a B2Store handles.
        tmp_file_path = self._create_local_tmp_file(path.name)
        with open(tmp_file_path, 'w') as f:
            json.dump(file, f)
        self.upload_file(tmp_file_path, path)
        os.remove(str(tmp_file_path))

    async def _write_blueprints(self, blueprints: Blueprints, path: Path) -> None:
        tmp_file_path = self._create_local_tmp_file(path.name)
        with open(tmp_file_path, 'w') as f:
            json.dump(blueprints.to_json(), f)
        self.upload_file(tmp_file_path, path)

    def download_file(
        self,
        b2_file_path: Path,
        local_bucket_path: str,
    ) -> None:
        try:
            self.b2.Bucket(self.bucket_name).download_file(
                str(b2_file_path), str(local_bucket_path)
            )
        except ClientError as ce:
            print("B2Store.download_file. Error: ", ce)

    def upload_file(
        self,
        src_file_path: Path,
        b2_file_path: Path,
    ) -> None:
        # TODO: parallel uploading to different upload URL's can
        # speed up the upload of files, per the B2 API docs:
        # https://www.backblaze.com/b2/docs/b2_get_upload_url.html
        try:
            response = self.b2.Bucket(self.bucket_name).upload_file(
                str(src_file_path), str(b2_file_path)
            )
        except ClientError as ce:
            print('error', ce)

        return response
