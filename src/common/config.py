import os

WELCOME_MESSAGE = os.getenv('WELCOME_MESSAGE', 'Hello World!')
LOCAL_PATH = os.getenv('LOCAL_PATH', '/Users/rchaks/Code/GitHub/bangla_reader/data')
LOCAL_CONTENT_FILENAME = os.getenv('LOCAL_CONTENT_FILENAME', 'legend.json')

STORAGE_ACCOUNT_NAME = os.getenv('STORAGE_ACCOUNT_NAME', 'bangladocumentstore')
STORAGE_ACCOUNT_KEY = os.getenv('STORAGE_ACCOUNT_KEY')
CONTAINER_NAME = os.getenv('CONTAINER_NAME', 'book-1')
DIRECTORY_PATH = os.getenv('DIRECTORY_PATH', 'img')

GCP_VISION_KEY = os.getenv('GCP_VISION_KEY')

BACKUP_CLIENT_ID = os.getenv('BACKUP_CLIENT_ID')
BACKUP_CLIENT_EMAIL = os.getenv('BACKUP_CLIENT_EMAIL')
BACKUP_PRIVATE_KEY_ID = os.getenv('BACKUP_PRIVATE_KEY_ID')
BACKUP_PRIVATE_KEY = os.getenv('BACKUP_PRIVATE_KEY')