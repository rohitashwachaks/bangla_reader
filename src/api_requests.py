import base64
import uuid
from threading import Thread

from flask import Blueprint, request, render_template

from src.clients.storage_client import StorageClient
from src.clients.vision_client import VisionAPI
from src.clients.speech_client import SpeechAPI

requests = Blueprint('requests', __name__)


@requests.route('/upload/', methods=['POST'])
def upload_image():
    filename = str(uuid.uuid4())
    StorageClient.upload_blob(data=request.data, filename=filename + '/img.jpeg')
    data = base64.b64encode(request.data).decode()

    ocr_response = VisionAPI.ocr_request(data)
    decoded_text = ocr_response['responses'][0]['fullTextAnnotation']['text']

    decoded_text = repr(decoded_text)[1:-1].replace('"', "'")
    StorageClient.upload_blob(data=decoded_text.encode(), filename=filename + '/OCR.txt')

    text = {}
    for index, sentence in enumerate(decoded_text.split(sep='।'), 1):
        text[index] = {'text': sentence}

    background_thread = Thread(target=SpeechAPI.synthesize, args=(filename, text, True))
    background_thread.start()

    return {
        'id': filename,
        'text': text
    }
#
# @requests.route('/synthesise/', methods=['POST'])
# def synthesize_voice():
#     speech_api.synthesize(img_name, res)

# @requests.route('/read/', methods=['GET'])
# def read_image(recording_id: str):
#     print(recording_id)
#     StorageClient.fetch_blob(recording_id)
