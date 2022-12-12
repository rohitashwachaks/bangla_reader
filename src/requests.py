import base64
import uuid

from flask import Blueprint, request, render_template

from src.clients.storage_client import StorageClient
from src.clients.vision_client import VisionAPI

requests = Blueprint('requests', __name__)


@requests.route('/upload/', methods=['POST'])
def upload_image():
    filename = str(uuid.uuid4())
    StorageClient.upload_blob(data=request.data, filename=filename + '/img.jpeg')
    data = base64.b64encode(request.data).decode()

    decoded_text = VisionAPI.ocr_request(data)
    decoded_text = decoded_text['responses'][0]['fullTextAnnotation']['text']

    decoded_text = repr(decoded_text)[1:-1].replace('"', "'")
    StorageClient.upload_blob(data=decoded_text.encode(), filename=filename + '/OCR.txt')
    return {
        'id': filename,
        'text': decoded_text
    }


@requests.route('/read/', methods=['GET'])
def read_image(recording_id: str):
    print(recording_id)
    StorageClient.fetch_blob(recording_id)
