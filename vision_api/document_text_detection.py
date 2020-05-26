import base64
import json
import os
import sys
from io import BytesIO
from PIL import Image
from requests import Session, Request


def pil_image_to_base64(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    str_encode_file = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return str_encode_file


def recognize_image(pil_image, key):
    str_encode_file = pil_image_to_base64(pil_image)
    str_url = "https://vision.googleapis.com/v1/images:annotate?key="
    str_api_key = key
    str_headers = {'Content-Type': 'application/json'}
    str_json_data = {
        'requests': [
            {
                'image': {
                    'content': str_encode_file
                },
                'features': [
                    {
                        'type': "DOCUMENT_TEXT_DETECTION",
                        'maxResults': 10
                    }
                ]
            }
        ]
    }

    obj_session = Session()
    obj_request = Request("POST",
                          str_url + str_api_key,
                          data=json.dumps(str_json_data),
                          headers=str_headers
                          )
    obj_prepped = obj_session.prepare_request(obj_request)
    obj_response = obj_session.send(obj_prepped,
                                    verify=True,
                                    timeout=60
                                    )

    if obj_response.status_code == 200:
        text = get_full_text_annotation(obj_response.text)
        return text
    else:
        return "error"


def get_full_text_annotation(json_data):
    text_dict = json.loads(json_data)
    text = text_dict["responses"][0]["fullTextAnnotation"]["text"]
    return text


if __name__ == '__main__':
    img_path = sys.argv[1]
    api_key = os.environ["GCP_VISION_SUBSCRIPTION_KEY"]
    img = Image.open(img_path)
    print(recognize_image(img, api_key))
