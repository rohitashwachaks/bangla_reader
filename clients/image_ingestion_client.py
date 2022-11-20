import io
import json
import os

from common.config import LOCAL_PATH, LEGEND_FILENAME, CONTAINER_NAME, STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY
from azure.storage.blob import BlobServiceClient


class ImageReaderClient:
    def __init__(self, local: bool = False) -> None:
        self._local = local
        self._legend = None
        blob_service_client = BlobServiceClient(
            account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=STORAGE_ACCOUNT_KEY)
        self._container_client = blob_service_client.get_container_client(container=CONTAINER_NAME)

        self.__load_legend__()

        self.__walk_blobs__()
        return

    def __load_legend__(self) -> None:
        try:
            if self._local:
                legend_filename = os.path.join(LOCAL_PATH, LEGEND_FILENAME)
                with open(legend_filename, 'r') as fp:
                    self._legend = json.load(fp)
            else:
                blob_client = self._container_client.get_blob_client(blob=LEGEND_FILENAME)
                data_stream = blob_client.download_blob()
                data_stream = data_stream.readall().decode()
                self._legend = json.loads(data_stream)
        except Exception as ex:
            print(f'Failed to load legend file.\n {ex}')

        return

    def __walk_blobs__(self) -> None:
        gen = self._container_client.walk_blobs()

        pass
    @property
    def legend(self):
        return self._legend
