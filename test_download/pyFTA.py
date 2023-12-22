import json

import requests

from moduls.slFTA import send_сmd

# from server import request_to_db

bmp_path = r'd:\Ivanov\browsermob-proxy-2.1.4\bin\browsermob-proxy'
drv_path = r'c:\chromedriver\chromedriver.exe'


def tst_execute(tst_num, trg, save_log):
    response = requests.get('http://127.0.0.1:8000/custom-response/',
                            params={'tst_num': 'testes_classes', 'trg': '240', 'save_log': 'True'})

    print(response)
    response['t_info']['tst_par']["drv_path"] = drv_path
    response['t_info']['tst_par']["bmp_path"] = bmp_path

    result = {"steps_result": dict()}

    # Пошаговое выполнение теста
    for step_num, cmd in enumerate(response['tst_arr']):
        print(
            f'=====================\n'
            f'cur_step ={response["t_info"]["cur_step"]}\n'
            f'cur_cmd ={response["t_info"]["cur_cmd"]}\n'
            f'{response}\n'
            f'=====================\n'
        )
        response["t_info"]['cur_step'] = step_num
        response['cur_cmd'] = cmd
        # print('+'*10, '\n', tst_info, '\n'*4, '+'*10)
        send_сmd(response)
        d = dict()
        d[step_num] = dict(cmd)
        result['steps_result'][step_num] = dict(d)

    response["result"] = result
    with open('jsons/result.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, default=lambda o: '<not serializable>', ensure_ascii=False, indent=4)


tst_execute(165, '240', True)  # 226
