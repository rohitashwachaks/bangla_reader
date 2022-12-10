import base64

from flask import Blueprint, request, render_template
from src.clients.vision_client import VisionAPI

image_upload = Blueprint('image_upload', __name__)


@image_upload.route('/upload/', methods=['POST'])
def upload_image():
    data = base64.b64encode(request.data).decode()
    decoded_text = VisionAPI.ocr_request(data)
    return decoded_text['responses'][0]['fullTextAnnotation']['text']
