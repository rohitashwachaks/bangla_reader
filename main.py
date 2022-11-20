

from clients.image_ingestion_client import ImageReaderClient

if __name__ == "__main__":
    image_reader_client = ImageReaderClient(local=True)
    image_reader_client.legend