import json

import requests

""" ДЛЯ БРАУЗЕРА ССЫЛКА: http://127.0.0.1:8000/custom-response/?tst_num=165&?trg=240&?save_log=True """

url = 'http://127.0.0.1:8000/custom-response/'
params = {'tst_num': '165', 'trg': '240', 'save_log': 'True'}

response = requests.get('http://127.0.0.1:8000/custom-response/',
                        params={'tst_num': '165', 'trg': '240', 'save_log': 'True'})

print(response.status_code, response.text)

with open(r'json_results/result_response_spec-api.json', 'w', encoding='utf-8') as file_json:
    file_json.write(json.dumps(response.json()))

print(response.json())  # Если ответ в формате JSON
