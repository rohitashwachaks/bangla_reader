import json

from clients.image_ingestion_client import ImageReaderClient
from common.speech_api import SpeechAPI
from common.vision_api import VisionAPI

if __name__ == "__main__":
    image_reader_client = ImageReaderClient(local=True, container_name='book-1')
    vision_api = VisionAPI()
    speech_api = SpeechAPI()

    response_dict = image_reader_client.content

    for img_name, content in image_reader_client.content.items():
        res = vision_api.ocr_request(content['content'])
        res = res['responses'][0]['textAnnotations'][0]['description']
        response_dict[img_name]['translation'] = res

        res = speech_api.synthesize(img_name, res)
        response_dict[img_name]['audio'] = res
    response_dict

    with open(image_reader_client.content_file, 'w') as fp:
        json.dump(response_dict, fp, indent=2)

    with open('data/book-1/failed_speech.json', 'w') as fp:
        json.dump(obj=speech_api.failed, indent=2, fp=fp)
