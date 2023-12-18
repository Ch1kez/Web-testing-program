import datetime
import time
import json
import random
import psycopg2
import uuid

import requests
import xml.etree.cElementTree as ET

import xml_cr_pts_240
import xml_cr_pts_243
import xml_new_owner
import xml_new_own_vtb


# Выполнение запроса и обновление результатов
def sel_qwr(qwr, srvbd):
	srvbd = srvbd.upper()
	if srvbd == 'СЭП 240':
		conn = psycopg2.connect(dbname='pts', user='postgres', password='postgres', host='sto-db-1c.elpts.local')
		# $cons = "host=10.17.10.131 port=5432 dbname=pts user=postgres password=postgres";
	elif srvbd == 'СЭП 243':
		conn = psycopg2.connect(dbname='pts', user='postgres', password='postgres', host='10.18.6.131')
		# $cons = "host=10.18.6.131 port=5432 dbname=pts user=postgres password=postgres"
	elif srvbd == 'EOTTS':
		conn = psycopg2.connect(dbname='otts', user='monitoring', password='monitoring', host='prot-eotts-db.elpts.local')
	else:
		print("#err Connection no definded")
	# Выполняем запрос

	cursor = conn.cursor()
	try:
		cursor.execute(qwr)
	except Exception as e:
		return [e]

	rdat = cursor.fetchall()

	cursor.close()
	conn.close()

	return rdat


# +++ Получение кода подтверждения из БД
def get_data_from_bd(zvl_num, qwr_num, trg='СЭП 240'):
	sql_q = """SELECT count(*) cnt FROM request.fdc_request req 
		left join notification.fdc_notification fn on fn.source_record_id = req.id 
		where request_number = '{0}' and fn.notification_text like '%Код%' 
		and fn.date_send notnull""".format(zvl_num)

	sql_s = """SELECT json_build_object('rnum', request_number, 
		'rcode', regexp_replace(fn.notification_text, '.*Код подтверждения |.$|. Код доступа.*$', '', 'g'),
		'dcode', regexp_replace(fn.notification_text, '.*Код доступа |.$|. Код залога.*$', '', 'g'), 
		'zcode' ,regexp_replace(fn.notification_text, '.*Код залога |.$', '', 'g')) jans 
		FROM request.fdc_request req 
		left join notification.fdc_notification fn on fn.source_record_id = req.id 
		where request_number = '{0}' and fn.notification_text like '%Код%' 
		order by fn.date_send desc limit 1""".format(zvl_num)
	ret_v = {}
	for i in range(60):
		cnt_q = sel_qwr(sql_q, trg)[0][0]
		if cnt_q >= int(qwr_num):
			ret_v = sel_qwr(sql_s, trg)[0][0]
			break
		time.sleep(1)
	return ret_v


def create_pts(pts_mask, tst_inf):
	# @@@ЭПТС@@@ПрефПерем@@@qtype=NewPEP или FOwnPEP&vmask=MZDGJ52Y8&tnum=tstN@@@

	s_mask = pts_mask.split('&')
	scmd = s_mask[0].replace('qtype=', '').replace('243', '').replace('240', '').replace('_', '')
	svin = s_mask[1].replace('vmask=', '')
	tnum = s_mask[2] if len(s_mask) > 2 else svin
	ret_v = {'vin': 'Ошибка создания ЭПТС', 'epts': 'Ошибка создания ЭПТС'}

	# Получаем уникальный VIN
	wrkvin = get_unic_vin(svin, tst_inf)
	print('Запрос на создание ЭПТС с vin: ' + wrkvin)

	# Отправляем запрос на создание ЭПТС
	create_pts_ws(tst_inf, scmd, wrkvin, tnum)
	# time.sleep(10)
	i = 0
	while i < 240:
		ptsnum = get_epts_by_vin(wrkvin, tst_inf)
		#  Если ПТС успешно создан
		if len(ptsnum) == 15:
			if scmd == 'FOwnPEP':
				new_owner(ptsnum, 'PEP', tst_inf)
			elif scmd == 'FOwnVTB':
				new_owner(ptsnum, 'VTB', tst_inf)
			ret_v = {'vin': wrkvin, 'epts': ptsnum}
			break
		i = i + 1
		time.sleep(1)
	return json.dumps(ret_v, ensure_ascii=False)


# Создание ЭПТС через сервис
def create_pts_ws(targ, ptstype, tsvin, stvin):
	cuuid = uuid.uuid4()
	cnd = "nd" + stvin + str(round(datetime.datetime.utcnow().timestamp()))
	cnsh = "nsh" + stvin + str(round(datetime.datetime.utcnow().timestamp()))
	cnk = "nk" + stvin + str(round(datetime.datetime.utcnow().timestamp()))
	cuveos = uveos()
	if (ptstype.endswith('PEP') or ptstype.endswith('VTB')):
		if targ == 'СЭП 240':
			prexml = xml_cr_pts_240.xml_crpts.format(cuuid, tsvin, cnd, cnsh, cnk, cuveos)
		else:
			prexml = xml_cr_pts_243.xml_crpts.format(cuuid, tsvin, cnd, cnsh, cnk, cuveos)
	send_xml(targ, prexml)


# Новый собственник через сервис
def new_owner(ptsn, own, targpl):
	cuuid = uuid.uuid4()
	mnem ='RUOWNER000089' if targpl == 'СЭП 240' else 'RUИЗГОТОВИТЕЛЬ000002'
	if (own == 'PEP'):
		prexml = xml_new_owner.xml_new_own.format(cuuid, ptsn, mnem)
	elif (own == 'VTB'):
		prexml = xml_new_own_vtb.xml_new_own_vtb.format(cuuid, ptsn, mnem)
	send_xml(targpl, prexml)


# Отправка XML
def send_xml(targp, xml_str):
	body = xml_str
	endpnt = 'http://10.17.10.31:8080/integration/services/epts' if targp == 'СЭП 240' else 'https://10.18.5.150/integration/services/epts'
	queueid = ''
	messgeid = ''
	sendtime = ''
	errorcode = ''
	body = body.encode('utf-8')
	session = requests.session()
	requests.packages.urllib3.disable_warnings()

	session.headers = {"Content-Type": "text/xml; charset=utf-8"}
	session.headers.update({"Content-Length": str(len(body))})
	try:
		response = session.post(url=endpnt, data=body, verify=False)
		if "No service was found" not in str(response.content):
			root = ET.fromstring(response.content)
			for child in root.iter():
				if "QueueID" in child.tag:
					queueid = child.text
				if "MessageID" in child.tag:
					messgeid = child.text
				if "SendingTimestamp" in child.tag:
					sendtime = child.text
				if "ErrorCode" in child.tag:
					errorcode = child.text
		else:
			raise SystemExit ("No service was found")
		#print(response.content)
	except requests.exceptions.RequestException as e:  # This is the correct syntax
		raise SystemExit(e)


# Генератор УВЭОС
def uveos():
	ccbk = (datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.random())[2:])[0:18]
	# ccbk = '202202031624245800'
	control = 0
	while control < 10:
		ccn = ccbk + str(control)
		c = [int(x) for x in ccn[::-2]]
		u2 = [(2*int(y))//10+(2*int(y)) % 10 for y in ccn[-2::-2]]
		value = sum(c+u2)
		if value % 10 == 0:
			break
		else:
			control += 1
	return ccn


# Формируем уникальный VIN, отсутствующий в БД
def get_unic_vin(maskv, targ):
	fmt = "{m}{n:0" + str(17 - len(maskv)) + "}"
	sql = "SELECT vin FROM pts.fdc_pts_ver where vin like '{0}%'".format(maskv)
	# tblv = sel_qwr(sql, targ)
	tblv = ('MZDGJ52Y800001654',)
	cnt = 1
	while True:
		nvin = fmt.format(m=maskv, n=cnt)
		if (nvin,) not in tblv:
			return nvin
		cnt = cnt + 1


# Получение номера ЭПТС по VIN
def get_epts_by_vin(nvin, targ):
	sql = """
		select epts_num from ( select * from (SELECT r.epts_num, 0 FROM pts.fdc_pts_ver v 
		left join pts.fdc_pts_root r on v.root_id = r.id 
		where vin = '{0}' union select '' epts_num, 1) t1 order by 2 limit 1) t2""".format(nvin)
	rtbl = sel_qwr(sql, targ)
	eptsn = rtbl[0][0] if rtbl[0][0] != None else ''
	return eptsn


# zz = get_data_from_bd('RU029230000000068', 1, 'СЭП 240')
# print(zz)
#get_epts_by_vin('MZDGJ52Y800001654', 'СЭП 240')
#zz = create_pts('qtype=FOwnVTB&vmask=MZDGJ52Y8&tnum=tstN', 'СЭП 240')
#print(zz)