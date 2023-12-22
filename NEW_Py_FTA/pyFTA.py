import json

from fnFTA import *
import requests
import random
import time

from datetime import datetime
from datetime import timedelta
from slFTA import send_сmd, wait_load_sep, wait_load_eotts, wait_end_ajax
from srFTA import create_pts


# Выполняем тест
def tst_execute(tst_data):
	client_cfg = open_data('D:/Ivanov/selenium/client_cfg.json')
	tst_info = tst_data['tst_info']
	tst_info['drv_path'] = client_cfg['drv_path']
	tst_info['plugins'] = client_cfg['plugins']
	tst_info['bmp_path'] = client_cfg['bmp_path']

	tst_array = tst_data['tst_arr']

	# Пошаговое выполнение теста
	for cmd in tst_array:
		tst_info['cur_step'] += 1
		tst_info['cur_cmd'] = cmd

		cf = (cmd['fnd'] if 'fnd' in cmd else '') + ((' : ' + cmd['key']) if 'key' in cmd else '')
		rm = cmd['rem'] if 'rem' in cmd else ''

		print("{0}: {1} ({2})".format(tst_info['cur_step'], cf, rm))

		send_сmd(tst_info)
		# ---------------------------------------------------------------------------
		if (str(cmd['fnd']).strip() if 'fnd' in cmd else '') == '@xpathNoProxy':
			time.sleep(1)
		elif tst_info['prx'] is not None:
			wait_end_ajax(tst_info, 2, tst_info['cur_step'])
			if str(tst_info['tsts']).startswith('СЭП'):
				wait_load_sep(tst_info['drv'])
			else:
				wait_load_eotts(False, "")
		# ---------------------------------------------------------------------------

		cs_log = tst_info['log_arr'][tst_info['cur_step'] - 1]
		rs = cs_log['res'] if 'res' in cs_log else ''

		print("... {0}".format(rs))

		rsc = cs_log['resc'] if 'res' in cs_log else -1
		if rsc == 6:
			break
	print(tst_info)


# Эмулятор сервера ФТА
def get_test(tst_num, trg):
	# Загрузка теста из БД
	tst_array = open_test_bd(tst_num)
	# Определение параметров теста
	tst_par = get_par_test(tst_array, trg)

	tst_var = {}
	# Конвертация теста для клиента
	dbg_print = True
	err_prep_test = False
	for t_cmd in tst_array:
		if 'get' in t_cmd:
			t_cmd['get'] = tst_par['tadr']
			if dbg_print:
				print(t_cmd)
		
		if 'fnd' in t_cmd:
			cfnd = t_cmd['fnd']
			rdy = ('xpath', '@Календарь', '@Радио', '@Селектор', '@ВДейств.')
			if cfnd not in rdy:
				if dbg_print:
					print("fnd: {0}".format(cfnd))

		if 'key' in t_cmd:
			s_key = str(t_cmd['key'])
			if s_key.startswith('@@@'):
				cmd = s_key.split("@@@")
				if cmd[1] == 'user':
					t_cmd['key'] = getUserCred(cmd[2], cmd[3], tst_par['tsts'])
				elif cmd[1] == 'ЭПТС':
					create_pts(cmd[3], tst_par['tsts'])

					# ----------------------------------------------------------
					ip = "10.17.15.45" if tst_par['dbg'] else "192.168.135.215"
					trg = "243" if str(tst_par['tsts']).endswith('243') else "240"
					url = "http://{0}/sc-new/scripts/ofa_tests.php?{1}&targ={2}".format(ip, cmd[3], trg)

					with requests.session() as sess:
						resp = sess.get(url, timeout=90).text
						ret_v = json.loads(resp)
						err_prep_test = 'id' in ret_v
						c_vin = ret_v["vin"] if 'vin' in ret_v else 'Ошибка создания ЭПТС'
						c_pts = ret_v["epts"] if 'epts' in ret_v else 'Ошибка создания ЭПТС'
						tst_var[cmd[2] + "_vin"] = c_vin
						tst_var[cmd[2] + "_epts"] = c_pts
					if dbg_print:
						print("Создан ЭПТС: {0} с VIN: {1}".format(c_pts, c_vin))
					# -----------------------------------------------------------
				elif cmd[1] == 'Random':
					add_p = ""
					while len(add_p) < int(cmd[3]):
						add_p += str(random.randint(0, 9))
					t_cmd['key'] = cmd[2] + add_p[0: int(cmd[3])]
					if dbg_print:
						print("Random: {0}".format(t_cmd['key']))
				elif cmd[1] == 'now':
					dt = datetime.now() + timedelta(int(cmd[3]) if len(cmd) > 3 else 0)
					t_cmd['key'] = dt.strftime(cmd[2].replace('yyyy', '%Y').replace('MM', '%m').replace('dd', '%d'))
					if dbg_print:
						print("Now: {0}".format(t_cmd['key']))
				else:
					if dbg_print:
						print("key: {0}".format(s_key))

		if 'cmd' in t_cmd:
			r_cmd = t_cmd['cmd'] 
			rdy = ['over', 'snd']
			if r_cmd not in rdy and dbg_print:
				print("cmd: {0}".format(r_cmd))
		
	tst_info = {
		'tsts': tst_par['tsts'],
		'tadr': tst_par['tadr'],
		'dbg': tst_par['dbg'],
		'headless': False,
		'var_arr': tst_var,
		'cur_step': 0,
		'drv': None,
		'prx': None,
		'log_arr': [],
		'log_ajax': {}
	}

	tst_data = {
		'tst_info': tst_info,
		'tst_arr': tst_array,
		'err_prep_test': err_prep_test
	}
	return json.dumps(tst_data, ensure_ascii=False)


# ------------------------------------------------------------------------------
# Проверенные тесты 143, testes_classes

# 209
rest_data = json.loads(get_test(209, '240'))
save_data('d:/Ivanov/selenium/BD/209.json', json.dumps(rest_data, ensure_ascii=False))

rest_data = json.loads(open_data('d:/Ivanov/selenium/BD/209.json'))

if not rest_data['err_prep_test']:
	tst_execute(rest_data)
