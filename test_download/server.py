import json
import sqlite3
from re import sub
from socket import gethostname

PATH_DB = r'D:\kurnaev.d\selenium\ftacommander.db'


# Выполнение запроса select к БД
def sel_sql(sql):
    with sqlite3.connect(PATH_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


def open_test_bd(test_id):
    tstrec = sel_sql('SELECT test_text FROM tests where id = {0}'.format(test_id))
    print(json.loads(tstrec[0][0]))
    return json.loads(tstrec[0][0])


# Признак тестовой площадки
def tfa_dbg():
    return gethostname() == 'sts-tf_tfa'


def get_par_test(t_array, trgp):
    retv = {'tsts': 'СЭП ' + trgp, 'dbg': tfa_dbg()}
    tst_start = ''
    eotts_macros = ["@ЗакрЭОТТС", "@ИнфЭОТТС", "@ПоискЭОТТС", "@РазворотЭОТТС", "@СвязиЭОТТС",
                    "@СелекторЭОТТС", "@ТаблЭОТТС", "@ПлюсЭОТТС", "@Прил2Настр_ЭОТТС", "@Прил2Зап_ЭОТТС",
                    "@Прил2Разд_ЭОТТС", "@Прил4_ЭОТТС", "@МинусЭОТТС", "@НастрЭОТТС", "@VIN_ЭОТТС", "@ЧекбоксЭОТТС"]

    # Ищем макросы ЭОТТС и определяем адрес площадки
    for cmd in t_array:
        if 'get' in cmd and tst_start == '':
            tst_start = cmd['get']
        if 'fnd' in cmd and cmd['fnd'] in eotts_macros:
            retv['tsts'] = 'ЭОТТС ' + trgp
    # Определяем адрес площадки
    int_ip = \
        sel_sql("SELECT {1}adr FROM Target where tname = '{0}'".format(retv['tsts'], 'd' if retv['dbg'] else 'm'))[0][0]
    retv['tadr'] = int_ip + sub('(?i)^http.+?\.\d{1,3}(:8080)?/', '/', tst_start)

    return retv

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def request_to_db( tst_num, trg, save_log):

    t_array = open_test_bd(tst_num)
    tst_info = {
        "t_info": {
            "tsts": "СЭП 240",
            "tadr": "http://10.17.10.31:8080/pts/login",
            "tst_par": get_par_test(t_array, trg),
            "dbg": True,
            "headless": False,
            "var_arr": {},
            "cur_step": 0,
            "cur_cmd": "",
            "drv": None,
            "prx": None,
            "log_arr": {},
            "log_ajax": {}
        },
        "tst_arr": open_test_bd(tst_num)
    }

    return tst_info



if __name__ == '__main__':
    # tst_num, trg, save_log = testes_classes, '240', True

    request = request_to_db(tst_num=165, trg='240', save_log=True)
    print(json.dumps(request))

    with open('jsons/qq.json', 'w', encoding='utf-8') as f:
        json.dump(request, f, default=lambda o: '<not serializable>', ensure_ascii=False, indent=4)


