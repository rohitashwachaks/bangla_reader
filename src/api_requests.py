import base64
import uuid
from threading import Thread

from flask import Blueprint, request, render_template

from src.clients.audio_player import WavReader
from src.clients.storage_client import StorageClient
from src.clients.vision_client import VisionAPI
from src.clients.speech_client import SpeechAPI

requests = Blueprint('requests', __name__)


@requests.route('/upload/', methods=['POST'])
def upload_image():
    filename = str(uuid.uuid4())
    print(f'Processing file: {filename}')
    StorageClient.upload_blob(data=request.data, filename=filename + '/img.jpeg')
    print(f'Img Uploaded: {filename}')

    data = base64.b64encode(request.data).decode()
    ocr_response = VisionAPI.ocr_request(data)
    print(f'OCR transcribed: {filename}')
    decoded_text = ocr_response['responses'][0]['fullTextAnnotation']['text']

    decoded_text = repr(decoded_text)[1:-1].replace('"', "'")
    StorageClient.upload_blob(data=decoded_text.encode(), filename=filename + '/OCR.txt')
    print(f'OCR Uploaded: {filename}')

    text = {}
    for index, sentence in enumerate(decoded_text.split(sep='।'), 1):
        text[index] = {'text': sentence}

    background_thread = Thread(target=SpeechAPI.synthesize, args=(filename, text, True))
    background_thread.start()
    print(f'Background Thread started: {filename}')

    return {
        'id': filename,
        'text': text
    }


@requests.route('/get_voice/', methods=['GET'])
def get_voice():
    filename = request.args.get('filename')
    data = StorageClient.fetch_blob(filename)
    background_thread = Thread(target=WavReader.play_audio, args=[data])
    background_thread.start()
    return data


@requests.route('/read/', methods=['POST'])
def read_speech():
    WavReader.play_audio(request.data)
    return 'Success'
