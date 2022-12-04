import requests
import json
from common.config import GCP_VISION_KEY


class VisionAPI:
    def __init__(self):
        self._url = f"https://vision.googleapis.com/v1/images:annotate?key={GCP_VISION_KEY}"
        self._payload = json.dumps({
                          "requests": [
                            {
                              "image": {
                                "content": 'CONTENT',
                              },
                              "features": [
                                {
                                  "type": "DOCUMENT_TEXT_DETECTION",
                                  "maxResults": 1
                                }
                              ]
                            }
                          ]
                        })
        self._headers = {
          'Content-Type': 'application/json'
        }
        return

    def __payload__(self, img):
        return self._payload.replace('CONTENT', img)

    def ocr_request(self, img: str):
        response = requests.request("POST", self._url, headers=self._headers, data=self.__payload__(img))
        return json.loads(response.content.decode())
