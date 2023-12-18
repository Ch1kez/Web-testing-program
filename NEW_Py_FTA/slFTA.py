from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime
import psutil
import traceback

from browsermobproxy import Server
from browsermobproxy import Client
from fnFTA import *

# Подготовка драйвера и прокси для теста
def prep_test(t_info):

	for proc in psutil.process_iter():
		# check whether the process name matches
		if proc.name() == "browsermob-proxy":
			proc.kill()

	server = Server(t_info['bmp_path'], options={'port': 9091})

	server.start()
	proxy_server = server.create_proxy()
	proxyConfig = Client.webdriver_proxy(proxy_server)

	opt = Options()
	opt.add_argument("--proxy-server={0}".format(proxy_server.proxy))
	opt.add_argument("--remote-allow-origins=*")
	if t_info['headless']:
		opt.add_argument("--headless=new")

	for p in t_info['plugins']:
		print('add plugin:' + p)
		#opt.add_extension("c:\\chromedriver\\1.2.8_0.crx")
		#opt.add_extension("c:\\chromedriver\\1.1_0.crx")

	drv = webdriver.Chrome(service=ChromeService(t_info['drv_path']), options=opt)
	drv.maximize_window()
	turl = t_info['tadr']
	drv.get(turl)
	proxy_server.new_har()
	t_info['drv'] = drv
	t_info['prx'] = proxy_server
	#t_info['log_arr'][t_info['cur_step']] =
	return "Открытие адреса " + turl

def elem_action(tst_info, fName, eIdx, eCmd, eSnd, cmdNotReq):
	driver = tst_info['drv']
	driver.implicitly_wait(2)
	cntRepeat = 0

	'''
	WebElement actEl;
	
	String fldTxt, varV;
	'''
	wait = WebDriverWait(driver, 10, 0.1)


	# Ищем элементы без учета индекса
	zzw = driver.find_elements(By.XPATH, fName)

	if len(zzw) == 0:
		write_log("Элемент не найден")
		return 6
	# Если элемент не виден и команда не обязательна выходим 
	zzo = zzw[0 if eIdx == -1 else eIdx]
	if not zzo.is_displayed() and cmdNotReq:
		write_log("Элемент не виден")
		return 6

	# Если индекс не указан и элементов болше 1 - проверяем сколько видно
	cntVisible = 0
	if eIdx == -1:
		for nE in range(len(zzw)):
			if zzw[nE].is_displayed():
				# Если элемент видим, устанавливаем его индекс и увеличиваем счетчик видимых
				eIdx = nE
				cntVisible += 1
		if cntVisible != 1:
			eIdx = 0

	if eCmd == "click":
		wait.until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, fName)[eIdx])).click()
	elif eCmd == "dblclick":
		ActionChains(driver).double_click(wait.until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, fName)[eIdx]))).perform()
		# (new Actions(driver)).doubleClick(wait.until(ExpectedConditions.elementToBeClickable(driver.findElements(fName).get(eIdx)))).perform()
		# raise Exception("Не реализовано")
	elif eCmd == "save":
		f_el = driver.find_elements(By.XPATH, fName)
		var_v = f_el[eIdx].get_attribute("innerText")
		if var_v == '':
			var_v = f_el[eIdx].get_attribute("value")
		# addVarToArray(eSnd, var_v)
		tst_info['var_arr'][eSnd] = var_v
		# raise Exception("Не реализовано")
	elif eCmd == "snd":
		if eSnd.startswith('Enter_'):
			#wait.until(ExpectedConditions.elementToBeClickable(driver.findElements(fName).get(eIdx))).sendKeys(eSnd.replace("Enter_", ""));
			#driver.findElements(fName).get(eIdx).sendKeys(Keys.ENTER);
			raise Exception("Не реализовано")
		elif eSnd.startswith('Tab_'):
			#wait.until(ExpectedConditions.elementToBeClickable(driver.findElements(fName).get(eIdx))).sendKeys(eSnd.replace("Tab_", ""));
			#driver.findElements(fName).get(eIdx).sendKeys(Keys.TAB);
			raise Exception("Не реализовано")
		elif eSnd.startswith('Clear_'):
			#actEl = driver.findElements(fName).get(eIdx);
			#actEl.click();
			#(new Actions(driver)).sendKeys(Keys.END).keyDown(Keys.SHIFT).sendKeys(Keys.HOME).keyUp(Keys.SHIFT).sendKeys(Keys.DELETE).perform();
			#wait.until(ExpectedConditions.elementToBeClickable(driver.findElements(fName).get(eIdx))).sendKeys(eSnd.replace("Clear_", ""));
			raise Exception("Не реализовано")
		elif eSnd.startswith('JS_'):
			#js.executeScript("arguments[0].value='" + eSnd.replace("JS_", "") + "';", driver.findElements(fName).get(eIdx));
			#driver.findElements(fName).get(eIdx).sendKeys(Keys.TAB);
			raise Exception("Не реализовано")
		else:
			wait.until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, fName)[eIdx])).send_keys(eSnd)
		while True:
			fldTxt = driver.find_elements(By.XPATH, fName)[eIdx].get_attribute("value")
			if fldTxt == eSnd or cntRepeat > 20:
				break
			time.sleep(0.1)
			cntRepeat += 1
	elif eCmd == "over":
		ActionChains(driver).move_to_element(driver.find_elements(By.XPATH, fName)[eIdx]).perform()


# Выполнение команды теста
def send_сmd(t_info):
	num_replay = '0'
	t_step = t_info['cur_cmd']
	tst_sep = t_info['tsts'].startswith('СЭП')
	to_log = {'stp': t_info['cur_step'], 'rem': (str(t_step['rem']).strip() if 'rem' in t_step else '')}

	if 'action' in t_step and t_step['action'] == 'Пропустить':
		to_log['res'] = "Пропущено"
		to_log['resc'] = 5
		t_info['log_arr'].append(to_log)
		return

	use_proxy = False
	cmd_not_required = "notrequired" in t_step

	v_fnd = str(t_step['fnd']).strip() if 'fnd' in t_step else ''

	if v_fnd != '@xpathNoProxy' and t_info['prx'] is not None:
		t_info['prx'].new_har()
		use_proxy = True
	elif v_fnd == '@xpathNoProxy':
		v_fnd = 'xpath'

	# -----------------------------------------------
	if "get" in t_step:  # Открываем стартовую страницу
		to_log['res'] = prep_test(t_info)
	elif v_fnd == "@ЖдатьДо": # Не реализовано. ждем наступления времени
		raise Exception("Не реализовано")
	else:
		m_drv: webdriver = t_info['drv']
		m_drv.implicitly_wait(2)
		wait = WebDriverWait(m_drv, 10, 0.1)
		sel_wait = WebDriverWait(m_drv, 10, 0.2);
		v_val = str(t_step['val']).strip()  if 'val' in t_step else ''
		v_cmd = str(t_step['cmd']).strip() if 'cmd' in t_step else 'click'
		nc_s_txt = str(t_step['key']).strip() if 'key' in t_step else ''
		s_act = str(t_step['action']).strip() if 'action'  in t_step else ''
		s_txt = prep_send_keys(nc_s_txt, t_info) # Предобработка ввода
		elem_idx = int(t_step['idx']) if 'idx' in t_step else -1
		simple_sel_type = True

		# Пауза перед выполнением команды
		wait_time = int(t_step["wait"]) if "wait" in t_step else 0

		# Пропускаем команды со своим ожиданием, перед остальными выполняем задержку
		if not (v_fnd.startswith("@Недост") or v_fnd.startswith("@Доступ") or v_fnd.startswith("@Значение")):
			if wait_time != 0:
				time.sleep(wait_time)

		# Если ЭОТТС - ждем недоступности элемента "Загрузка"
		# if (jRBMIEotts239.isSelected()) { waitLoadEotts(false, ""); }

		# TODO xpath
		if v_fnd == "xpath":  # ---
			try:
				elem_action(t_info, v_val.replace("[replay]", num_replay), elem_idx, v_cmd, s_txt, cmd_not_required)
				to_log['res'] = "Выполнено"
				to_log['resc'] = 0
				t_info['log_arr'].append(to_log)
				return
			except Exception as err:
				to_log['res'] = "Ошибка ({0})".format(traceback.format_exc())
				to_log['resc'] = 6
				t_info['log_arr'].append(to_log)
				return
		# INFO Реализовано
		elif v_fnd == "@СоздатьПТС":
			to_log['res'] = "Пропущено"
			to_log['resc'] = 5
			t_info['log_arr'].append(to_log)
			return
		# INFO Реализовано
		elif v_fnd == "@Календарь":
			try:
				ActionChains(m_drv).move_to_element(m_drv.find_element(By.XPATH, v_val)).perform()
				# Ищем Input за меткой
				n_xpath = (v_val + "/ancestor::div[contains(@class,'col-sm-8') or " +
					"contains(@class,'col-sm-4') or contains(@class,'col-xs-6') or " +
					"contains(@class,'row')][position()=1]//input[contains(@class,'hasDatepicker')]")
				m_drv.find_element(By.XPATH, n_xpath).click()
				ActionChains(m_drv).send_keys(Keys.END).key_down(Keys.SHIFT).send_keys(Keys.HOME).key_up(Keys.SHIFT).send_keys(Keys.DELETE).perform()
				wait_end_ajax(t_info, 2, t_info['cur_step'])
				wait.until(EC.element_to_be_clickable(m_drv.find_element(By.XPATH, n_xpath))).send_keys(s_txt)
				n_xpath = "//a[contains(@class,'ui-state-active')]"
				wait.until(EC.element_to_be_clickable(m_drv.find_element(By.XPATH, n_xpath))).click()
				to_log['res'] = "Выполнено"
				to_log['resc'] = 0
				t_info['log_arr'].append(to_log)
				return
			except Exception as err:
				to_log['res'] = "Ошибка ({0})".format(traceback.format_exc())
				to_log['resc'] = 6
				t_info['log_arr'].append(to_log)
				return
		# INFO Реализовано
		elif v_fnd == "@Радио":
			try:
				n_xpath = v_val + "/ancestor::label[position()=1]/label[contains(@class,'option-custom')]"
				wait.until(EC.element_to_be_clickable(m_drv.find_element(By.XPATH, v_val))).click()
				cnt_rep = 0
				while True:
					if m_drv.find_element(By.XPATH, n_xpath + "/input").get_attribute("checked") == "true":
						to_log['res'] = "Выполнено"
						to_log['resc'] = 0
						t_info['log_arr'].append(to_log)
						return
					time.sleep(0.1)
					cnt_rep += 1
					if cnt_rep > 20:
						break
				to_log['res'] = "... Ошибка ({0})".format("Больше 20 попыток")
				to_log['resc'] = 6
				t_info['log_arr'].append(to_log)
				return
			except Exception as err:
				to_log['res'] = "... Ошибка ({0})".format(err)
				to_log['resc'] = 6
				t_info['log_arr'].append(to_log)
				return
		# INFO Реализовано
		elif v_fnd == "@Сохр.перем.":
			try:
				save_data(s_txt, t_info['var_arr'])
				to_log['res'] = "Выполнено"
				to_log['resc'] = 0
				t_info['log_arr'].append(to_log)
				return
			except Exception as err:
				to_log['res'] = "... Ошибка ({0})".format(err)
				to_log['resc'] = 6
				t_info['log_arr'].append(to_log)
				return
		# INFO Реализовано
		elif v_fnd == "@ВТабл." or v_fnd == "@СТабл.":
			try:
				# Ищем чекбокс в строке с заявлением
				n_xpath = "//*[contains(text(), '" + s_txt + "')]/ancestor::tr//input[@type='checkbox']"
				if v_fnd == "@СТабл.":
					n_xpath = "//tbody[contains(@wicketpath,'results_body')]/tr[position()=" + s_txt + "]//input[@type='checkbox']"
				wait.until(EC.element_to_be_clickable(m_drv.find_element(By.XPATH, n_xpath))).click()
				to_log['res'] = "Выполнено"
				to_log['resc'] = 0
				t_info['log_arr'].append(to_log)
				return
			except Exception as err:
				to_log['res'] = "... Ошибка ({0})".format(err)
				to_log['resc'] = 6
				t_info['log_arr'].append(to_log)
				return
		# INFO Реализовано
		elif v_fnd == "@Селектор" or v_fnd == "@Селектор2":  # ---
			try:
				# Ищем простой селектор за меткой
				try:
					n_xpath = (v_val + "/ancestor::div[contains(@class,'col-sm-8') or contains(@class,'col-sm-6') or " +
						"contains(@class,'col-sm-4') or contains(@class,'row')][position()=1]//select/option[text() = '" +
						s_txt + "']")
					m_drv.find_element(By.XPATH, n_xpath).click()
					wait_end_ajax(t_info, 2, "simpl_sel")
					to_log['res'] = "Выполнено"
					to_log['resc'] = 0
					t_info['log_arr'].append(to_log)
					return
				except:
					simple_sel_type = False

				if not simple_sel_type:
					# Обрабатываем сложный селектор
					n_xpath = (v_val + "/ancestor::div[contains(@class,'col-sm-8') or contains(@class,'col-sm-6') " +
						"or contains(@class,'col-sm-4') or contains(@class,'row')][position()=1]//span[@class='selection']/span")
					if v_fnd == "@Селектор2":
						n_xpath = "((" + v_val + ")[position()=1])//ancestor::div[position()=1]//span[@class='selection']/span"

					# Очищаем значения при необходимости
					if s_txt.startswith("Clear_"):
						fdel = n_xpath + "//span[contains(@class,'select2-selection__clear')]"
						while True:
							if len(m_drv.find_elements(By.XPATH, fdel)) == 0:
								break
							ActionChains(m_drv).move_to_element(m_drv.find_element(By.XPATH, fdel + "[position()=1]")).perform()
							sel_wait.until(EC.element_to_be_clickable(m_drv.find_element(By.XPATH, fdel + "[position()=1]"))).click()
							s_txt = s_txt.replace("Clear_", s_act)
							if s_txt == '':
								to_log['res'] = "Выполнено"
								to_log['resc'] = 0
								t_info['log_arr'].append(to_log)
								return
					sel_wait.until(EC.visibility_of(m_drv.find_element(By.XPATH, n_xpath))).click()
					# Находим нужное поисковое поле
					css_search_window = ("(//span[@class='select2-container select2-container--default select2-container--open']//input|" +
										 v_val + "/following-sibling::span//input)")
					t_el = m_drv.find_element(By.XPATH, css_search_window)
					crazy_logic = []
					if "###" in s_txt:
						crazy_logic = s_txt.split("###")
						s_txt = crazy_logic[0]
						cmp_val = crazy_logic[1]
					else:
						cmp_val = s_txt

					if t_el.is_displayed():
						t_el.send_keys(s_txt)
						wait_end_ajax(t_info, 2, "Ожидание загрузки справочников")
						v_tst = m_drv.find_element(By.XPATH, css_search_window).get_attribute("value")
					else:
						v_tst = s_txt

					wait_end_ajax(t_info, 2, "пауза перед проверкой результатов")

					# Проверяем результат выбора селектора ?????????????
					cnt_rep = 0
					# To try -----------------------------------
					while True:
						cnt_rep += 1
						if cnt_rep > 2:
							break

						# Проверка окончания загрузки справочников
						css_res_window = ("//span[@class='select2-container select2-container--default select2-container--open']//" +
										"li[text()='Загрузка данных…'][@role='treeitem']")
						while True:
							tstArr = m_drv.find_elements(By.XPATH, css_res_window)
							if len(tstArr) == 0:
								break
							ActionChains(m_drv).move_to_element(tstArr[0]).perform()
						# -------------------------------------------
						if elem_idx == -1:
							css_res_window = ("//span[@class='select2-container select2-container--default select2-container--open']//" +
											"li[text()='" + cmp_val + "'][@role='treeitem']")
							sel_wait.until(EC.visibility_of(m_drv.find_elements(By.XPATH, css_res_window)[0])).click()
						else:
							css_res_window = ("//span[@class='select2-container select2-container--default select2-container--open']//" +
											  "li[contains(text(),'" + cmp_val + "')][@role='treeitem']")
							#selWait.until(ExpectedConditions.visibilityOf(driver.findElements(By.xpath(css_res_window)).get(elemIndex))).click()
							sel_wait.until(EC.visibility_of(m_drv.find_elements(By.XPATH, css_res_window)[elem_idx])).click()

						wait_end_ajax(t_info, 2, "Сравнение результатов")

						v_tst = m_drv.find_element(By.XPATH, n_xpath).get_attribute("innerText")
						if s_txt in v_tst or cmp_val in v_tst:
							to_log['res'] = "Выполнено"
							to_log['resc'] = 0
							t_info['log_arr'].append(to_log)
							return
						# End To try -----------------------------------
					to_log['res'] = "Ошибка"
					to_log['resc'] = 6
					t_info['log_arr'].append(to_log)
					return
				to_log['res'] = "Выполнено"
				to_log['resc'] = 0
				t_info['log_arr'].append(to_log)
				return
			except Exception as err:
				to_log['res'] = "Ошибка ({0})".format(err)
				to_log['resc'] = 6
				t_info['log_arr'].append(to_log)
				return
		# INFO Реализовано
		elif v_fnd == "@ВДейств.":  # ---
			try:
				# Ищем Input за меткой
				menu_root = "//button[contains(@class,'btn-base')][contains(@class,'dropdown-toggle')][@data-toggle='dropdown']"
				sel_wait.until(EC.element_to_be_clickable(m_drv.find_elements(By.XPATH, menu_root)[0 if elem_idx == -1 else elem_idx])).click()
				if m_drv.find_element(By.XPATH, v_val).is_displayed():  # Конечный элемент меню - видим
					sel_wait.until(EC.element_to_be_clickable(m_drv.find_element(By.XPATH, v_val))).click()
				else:  # Конечный элемент  - a
					# Ищем элемент подменю
					menu_sub = v_val + "/ancestor::li[contains(@class,'item-with-sub-menu')]"
					# new Actions(driver).moveToElement(selWait.until(ExpectedConditions.elementToBeClickable(By.xpath(menu_sub)))).perform();
					ActionChains(m_drv).move_to_element(sel_wait.until(EC.element_to_be_clickable(m_drv.find_element(By.XPATH, menu_sub)))).perform()
					if not m_drv.find_element(By.XPATH, v_val).is_displayed():
						# js.executeScript("window.scrollBy(0,50);")
						raise Exception("Не реализовано")
					m_drv.find_element(By.XPATH, v_val).send_keys(Keys.ENTER)

				to_log['res'] = "Выполнено"
				to_log['resc'] = 0
				t_info['log_arr'].append(to_log)
				return
			except Exception as err:
				to_log['res'] = "Ошибка ({0})".format(err)
				to_log['resc'] = 6
				t_info['log_arr'].append(to_log)
				return

	#---------------------------------------------------------------------------
		'''
		if v_fnd == '@xpathNoProxy':
			time.sleep(wait_time)
		elif t_info['prx'] != None:
			wait_end_ajax(t_info, 2, t_info['cur_step'])
			if tst_sep:
				wait_load_sep(t_info['drv'])
			else:
				wait_load_eotts(False, "")
		'''

	# Запись в массив лога
	to_log['res'] = "Выполнено"
	to_log['resc'] = 0
	t_info['log_arr'].append(to_log)
	# return 0


# Ожидание выполнения запросов, путем анализа пакетов, прошедших прокси-сервер
def wait_end_ajax(tst_inf, wait_time_sec, rem):
	bmp_prx = tst_inf['prx']
	prev_cnt = 0
	curr_cnt = 0
	cnt_rep = 0

	start_w = datetime.datetime.now()

	while True:
		time.sleep(0.25)

		curr_cnt = len(bmp_prx.har['log']['entries'] )
		cnt_rep += 1
		if curr_cnt > prev_cnt :
			prev_cnt = curr_cnt
			cnt_rep = 0
		if cnt_rep > 3:
			break
	sum0 = 0
	curr_cnt = 0
	sum_err = 0

	for h in bmp_prx.har['log']['entries']:
		if str(h['serverIPAddress']).startswith('10.') or str(h['serverIPAddress']).startswith('192.168.'):
			curr_cnt += 1
			stQ = h['response']['status']
			if stQ == 0:
				sum0 += 1
			elif stQ == 200:
				pass
			else:
				sum_err += 1
	end_w = datetime.datetime.now()
	qwr_d = end_w - start_w
	dlt = int(qwr_d.microseconds / 1000)
	str_log = "XHR: {0} ({1}); Time: {2} ms; No200: {3}; NoResp: {4};".format(curr_cnt, cnt_rep, dlt, sum_err, sum0)
	tst_inf['log_ajax'][rem] = str_log
	#print(str_log)


# Ожидание загрузки в СЭП
def wait_load_sep(driver):
	cnt_rep = 0
	n_xpath = "//div[contains(@class, 'loader')][contains(@class, 'active')]"
	while True:
		time.sleep(0.1)

		zz = driver.find_elements(By.XPATH, n_xpath)
		if len(zz) > 0:
			if zz[0].is_displayed() or zz[0].is_enabled():
				cnt_rep += 1
			else:
				break
		elif cnt_rep > 1200:
			break
		else:
			break


		'''
		if len(zz) == 0:
			break
		elif not zz[0].is_displayed() or not zz[0].is_enabled():
			break
		elif cnt_rep > 1200:
			# write_log( "... Загрузка больше 2 мин.")
			break
		time.sleep(0.1)
		cnt_rep += 1
		'''


# Ожидание загрузки в ЭОТТС
def wait_load_eotts(par1, par2):
	raise Exception("Не реализовано")