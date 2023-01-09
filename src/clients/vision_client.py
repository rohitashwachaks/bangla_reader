import requests
import json
from src.common.config import GCP_VISION_KEY


class VisionAPI:
    __url = f"https://vision.googleapis.com/v1/images:annotate?key={GCP_VISION_KEY}"
    __payload = json.dumps({
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
    __headers = {
        'Content-Type': 'application/json'
    }

    @staticmethod
    def __payload__(img):
        return VisionAPI.__payload.replace('CONTENT', img)

    @staticmethod
    def ocr_request(img: str):
        response = requests.request("POST", url=VisionAPI.__url, headers=VisionAPI.__headers,
                                    data=VisionAPI.__payload__(img))
        return json.loads(response.content.decode())
