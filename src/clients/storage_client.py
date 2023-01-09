import io
import json

from google.cloud import storage
from google.cloud.storage import Blob
from src.common.config import GCP_STORAGE_CREDENTIALS


class StorageClient:
    credentials_dict = json.loads(GCP_STORAGE_CREDENTIALS)

    __client = storage.Client.from_service_account_info(credentials_dict)
    __bucket = __client.get_bucket('bangla-reader')

    @staticmethod
    def upload_blob(data, filename: str, ):
        blob: Blob = StorageClient.__bucket.blob(filename)
        with io.BytesIO() as fp:
            fp.write(data)
            fp.seek(0)
            blob.upload_from_file(fp)
        return

    @staticmethod
    def fetch_blob(blob_id: str):
        blob: Blob = StorageClient.__bucket.get_blob(blob_name=blob_id)
        data = blob.download_as_bytes()
        return data
