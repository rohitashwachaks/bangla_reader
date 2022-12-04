import base64
import os
import webbrowser

import requests
import json
from tqdm import tqdm
from common.config import GCP_VISION_KEY


class SpeechAPI:
    def __init__(self):
        self.failed = {}
        self._url = f"https://texttospeech.googleapis.com/v1beta1/text:synthesize?key={GCP_VISION_KEY}"
        self._payload = json.dumps({
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
        self._headers = {
          'Content-Type': 'application/json'
        }
        return

    def __payload__(self, text):
        return self._payload.replace('CONTENT', text)

    def synthesize(self, img_name: str, text: str):
        text = repr(text)[1:-1].replace('"', "'").split('।')
        for number, sentence in (pbar := tqdm(enumerate(text, 1))):
            pbar.set_description(f'{img_name}/{str(number).zfill(2)}.wav')
            data = self.__payload__(sentence)
            response = requests.request("POST", self._url, headers=self._headers, data=data.encode('utf-8'))
            if response.status_code == 200:
                res = json.loads(response.content.decode())['audioContent']
                content = base64.b64decode(res)
                filename = f'data/book-1/{img_name}/{str(number).zfill(2)}.wav'
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                webbrowser.open(filename)
                with open(filename, 'wb') as fp:
                    fp.write(content)
            else:
                error_msg = json.loads(response.content.decode())['message']
                self.failed[img_name] = {
                    'index': number,
                    'sentence': sentence,
                    'error': error_msg
                }

        return res
