import base64
import os
import webbrowser

import requests
import json
from tqdm import tqdm

from src.clients.storage_client import StorageClient
from src.common.config import GCP_VISION_KEY


class SpeechAPI:
    __failed = {}
    __url = f"https://texttospeech.googleapis.com/v1beta1/text:synthesize?key={GCP_VISION_KEY}"
    __payload = json.dumps({
        "audioConfig": {
            "audioEncoding": "LINEAR16",
            "pitch": 0,
            "speakingRate": 0.9
        },
        "input": {
            "text": "CONTENT"
        },
        "voice": {
            "languageCode": "bn-IN",
            "name": "bn-IN-Wavenet-A"
        }
    })
    __headers = {
        'Content-Type': 'application/json'
    }

    @staticmethod
    def __payload__(text):
        return SpeechAPI.__payload.replace('CONTENT', text)

    @staticmethod
    def synthesize(img_name: str, text: dict, local=False):
        res = None
        pbar = tqdm(text.items())
        for number, sentence in pbar:
            pbar.set_description(f'{img_name}/{str(number).zfill(2)}.wav')
            text = sentence.get('text', '')
            data = SpeechAPI.__payload__(sentence)
            response = requests.request("POST",
                                        url=SpeechAPI.__url,
                                        headers=SpeechAPI.__headers,
                                        data=data.encode('utf-8')
                                        )

            if response.status_code == 200:
                res = json.loads(response.content.decode())['audioContent']
                content = base64.b64decode(res)
                filename = f'data/book-1/{img_name}/{str(number).zfill(2)}.wav'
                StorageClient.upload_blob(data=content, filename=f'{img_name}/{str(number).zfill(2)}.wav')
                if local:
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, 'wb') as fp:
                        fp.write(content)
                    webbrowser.open(filename)
            else:
                error_msg = json.loads(response.content.decode())['message']
                SpeechAPI.__failed[img_name] = {
                    'index': number,
                    'sentence': sentence,
                    'error': error_msg
                }
        return res
