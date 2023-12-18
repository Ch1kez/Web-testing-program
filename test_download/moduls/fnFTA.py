import json
import re
import sqlite3
import requests
import socket

fta_bd = r'D:\kurnaev.d\selenium\ftacommander.db'


# -------------------- Задействованные функции ----------------------

# Открываем тест из БД
def open_test_bd(test_id):
    tstrec = sel_sql('SELECT test_text FROM tests where id = {0}'.format(test_id))
    return json.loads(tstrec[0][0])


# Признак тестовой площадки
def tfa_dbg():
    return socket.gethostname() == 'sts-tf_tfa'


# Определение параметров теста
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
    retv['tadr'] = int_ip + re.sub('(?i)^http.+?\.\d{1,3}(:8080)?/', '/', tst_start)

    return retv


# ---------------------------------------------------------------------

# Открываем тест из файла
def open_test(file_name):
    with open(file_name, 'r', encoding="utf-8") as json_file:
        return json.load(json_file)


# Выполнение запроса select к БД
def sel_sql(sql):
    with sqlite3.connect(fta_bd) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


def bak_selTarget(add):
    return 'http://10.17.10.31:8080' + add


def save_log(cmd):
    print('Пишем лог в БД: ' + str(cmd))
    pass


def write_log(txt):
    print(txt)


def getUserCred(credVal, userN, target):
    sql = "select {0} retv from tuser where target = '{2}' and uorg = '{1}';".format(
        'ulogin' if credVal == 'login' else 'upass', userN, target)
    usrrec = sel_sql(sql)
    return usrrec[0][0]


# Извлечение переменной из массива
def getVarFromArray(varName):
    global varArr
    return str(varArr[varName]) if varName in varArr else "переменная не определена"


def prep_send_keys(inp_txt, tst_info):
    # global varArr
    '''
            String intvar, rvar, retV, numQ, addP;
        VarGen varG = new VarGen();
        JSONObject nVar = new JSONObject();
        Pattern pattern = Pattern.compile("\\[\\[\\[.*\\]\\]\\]");
        inp_txt = inp_txt.replace("[replay]", numReplay);
        Matcher matcher = pattern.matcher(inp_txt);
        if (matcher.find()) {
            intvar = matcher.group(0);
            rvar = prepSendKeys(intvar.replace("[[[", "").replace("]]]", ""));
            inp_txt = inp_txt.replace(intvar, rvar);
        }
    '''
    retV = str(inp_txt)
    if retV.startswith('@@@'):
        cmd = retV.split("@@@")
        val = []
        if cmd[1] == "now":  # --- Формируем дату
            '''
            Calendar v_date = Calendar.getInstance();
                SimpleDateFormat fmt_to_input = new SimpleDateFormat(cmd[2]);
                v_date.setTime(new Date());
                // вычисляем нужную дату
                if (cmd.length == 4) {
                    v_date.add(Calendar.DATE, Integer.parseInt(cmd[3]));
                }
                retV = fmt_to_input.format(v_date.getTime());
            '''
            pass
        elif cmd[1] == "ИзСписка":  # ---
            # val = cmd[2].split("#");
            # retV = val[(int)Math.floor(Math.random()*(val.length))];
            pass
        elif cmd[1] == "Файл":  # +++ Выделяем фрагмент имени файла и время ожидания
            retV = cmd[2] + "#" + cmd[4]
        elif cmd[1] == "ГенераторID":  # ---
            # retV = genRndID(cmd[2]);
            pass
        elif cmd[1] == "Задать":  # +++
            retV = cmd[2] + ";" + cmd[3] + ";"
        elif cmd[1] == "user":  # +++
            retV = getUserCred(cmd[2], cmd[3], tst_info['tst_par']['tsts'])
        elif cmd[1] == "ИнфЭОТТС":  # +++
            retV = cmd[2]
        elif cmd[1] == "ЭПТС":  # +++
            retV = inp_txt
        elif cmd[1] == "Повтор":  # +++
            retV = inp_txt;
        elif cmd[1] == "time":  # --- Формируем время
            '''
            Calendar v_date = Calendar.getInstance();
                SimpleDateFormat fmt_to_input = new SimpleDateFormat(cmd[2]);
                v_date.setTime(new Date());
                // вычисляем нужную дату
                if (cmd.length == 4) {
                    v_date.add(Calendar.MINUTE, Integer.parseInt(cmd[3]));
                }
                retV = fmt_to_input.format(v_date.getTime());
            '''
            pass
        elif cmd[1] == "УВЭОС":  # --- Формируем УВЭОС
            '''
            retV = varG.getUVEOS("")
            '''
            pass
        elif cmd[1] == "СНИЛС":  # --- Формируем СНИЛС
            '''
            retV = varG.getSNILS("");
            '''
            pass
        elif str(cmd[1]).startswith("КодПодтверждения"):  # --- Запрашиваем код подтверждения из БД
            '''
                numQ = "1";
                if (!cmd[1].equals("КодПодтверждения")) {
                    numQ = cmd[1].substring(cmd[1].length() - 1);
                }
                //String numQ = cmd[1]== "КодПодтверждения" ? "1" : cmd[1].substring(cmd[1].length() - 1);
                
                
                if(cmd.length == 3) {
                    retV = getDataFromBD(cmd[2], numQ).get("rcode").toString();
                }
                else if (cmd[3].equals("залога"))
                {
                    retV = getDataFromBD(cmd[2], numQ).get("zcode").toString();
                }
                else if (cmd[3].equals("доступа"))
                {
                    retV = getDataFromBD(cmd[2], numQ).get("dcode").toString();
                }
            '''
            pass
        elif cmd[1] == "Random":  # --- Формируем случайный номер
            '''
            addP = "";
                while (addP.length() <  Integer.parseInt(cmd[3]))
                {
                    addP += String.valueOf(Math.random()).substring(2);
                }
                retV = cmd[2] + addP.substring(0, Integer.parseInt(cmd[3]));
            '''
            pass
        elif cmd[1] == "var":  # --- Выбираем переменную из журнала
            retV = str(tst_info['var_arr'][cmd[2]]) if cmd[2] in tst_info['var_arr'] else "переменная не определена"
            if len(cmd) > 3:
                # retV = Character.toString(getVarFromArray(cmd[2]).charAt(Integer.parseInt(cmd[3]) - 1))
                pass

        elif cmd[1] == "2var":  # --- Сохраняем переменную в журнал при передаче текста элементу
            '''
            if (cmd.length == 4) {
                    nVar.put(cmd[2], cmd[3]);
                    varArr.add(nVar);
                    retV = cmd[3];
                }
            '''
            pass
        elif cmd[1] == "Table":  # +++ Формируем строку с адресом ячейки и именем переменной
            retV = cmd[2] + ";" + cmd[3] + ";" + cmd[4] + ";"
        else:  # +++ Имя переменной
            retV = cmd[1]

    return retV


# Создание ЭПТС для тестов через вэб-сервис
# @@@ЭПТС@@@ПрефПерем@@@qtype=СоздПЕП или ПСобствПЕП&vmask=MZDGJ52Y8@@@
def create_pts(tst_inf, pts_mask):
    qwrMask = pts_mask.split("@@@")
    ip = "10.17.15.45" if tst_inf['tst_par']['dbg'] else "192.168.135.215"
    trg = "243" if str(tst_inf['tst_par']['tsts']).endswith('243') else "240"

    url = "http://{0}/sc-new/scripts/ofa_tests.php?{1}&targ={2}".format(ip, qwrMask[3], trg)

    sess = requests.session()
    resp = sess.get(url, timeout=90).text
    retV = json.loads(resp)
    tst_inf['var_arr'][qwrMask[2] + "_vin"] = retV["vin"]
    tst_inf['var_arr'][qwrMask[2] + "_epts"] = retV["epts"]
    write_log("Создан ЭПТС: " + retV["epts"] + " с VIN: " + retV["vin"])
