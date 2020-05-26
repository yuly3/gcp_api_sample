import json
from requests import Session, Request


def text_translate(original_text, api_key):
    str_url = "https://translation.googleapis.com/language/translate/v2?key="
    str_headers = {'Content-Type': 'application/json'}
    str_json_data = {
        'q': original_text,
        'target': 'ja',
        'model': 'base'
    }
    
    obj_session = Session()
    obj_request = Request("POST",
                          str_url + api_key,
                          data=json.dumps(str_json_data),
                          headers=str_headers
                          )
    obj_prepped = obj_session.prepare_request(obj_request)
    obj_response = obj_session.send(obj_prepped,
                                    verify=True,
                                    timeout=60
                                    )
    
    if obj_response.status_code == 200:
        text_dict = json.loads(obj_response.text)
        return text_dict
    else:
        return obj_response.status_code


if __name__ == '__main__':
    # 以下で翻訳する英語のテキストと認証用APIキーを設定
    global_original_text = ''
    global_api_key = ''
    print(text_translate(global_original_text, global_api_key))
