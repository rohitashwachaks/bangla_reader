import base64
import io
import json
import os
from typing import Union

from tqdm import tqdm

from common.config import LOCAL_PATH, LOCAL_CONTENT_FILENAME, CONTAINER_NAME, STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY,\
    LOCAL_CONTENT_FILENAME
from azure.storage.blob import BlobServiceClient, BlobClient


class ImageReaderClient:
    def __init__(self, local: bool = False, container_name: Union[None, str]= None) -> None:
        self._legend = None
        self._content = {}
        self._local = local

        blob_service_client = BlobServiceClient(
            account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=STORAGE_ACCOUNT_KEY)

        container_name = CONTAINER_NAME if container_name is None else container_name
        self._container_client = blob_service_client.get_container_client(container=container_name)

        local_content_file = os.path.join(LOCAL_PATH, CONTAINER_NAME, LOCAL_CONTENT_FILENAME)
        if local:
            if not os.path.exists(local_content_file):
                local = False
                print('Local content file not found. Going online')
                local_content_folder = '/'.join(local_content_file.split('/')[:-1])
                os.makedirs(local_content_folder, exist_ok=True)
        self._local_content_file = local_content_file

        if local:
            with open(local_content_file, 'r') as fp:
                self._content = json.load(fp)

        else:
            self.__walk_blobs__()

        return

    def __walk_blobs__(self) -> None:
        gen = self._container_client.list_blobs()
        for file in (pbar := tqdm(gen)):
            pbar.set_description(file.name)
            blob_client: BlobClient = self._container_client.get_blob_client(blob=file.name)
            content = base64.b64encode(blob_client.download_blob().readall()).decode()
            file_name = '.'.join(file.name.split('.')[:-1])
            self._content[file_name] = {
                'content': content
            }
        return

    @property
    def content(self):
        return self._content

    @property
    def content_file(self):
        return self._local_content_file
