# from varFTA import *
from fnFTA import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait
import time
import psutil

from browsermobproxy import Server
from browsermobproxy import Client
#from browsermobproxy import *




# Подготовка драйвера и прокси для теста
def prepTest(startUrl):
	#global driver
	for proc in psutil.process_iter():
		# check whether the process name matches
		if proc.name() == "browsermob-proxy":
			proc.kill()

	server = Server(bmp_path, options = {'port': 9091})
	#server = Server('d:\\Ivanov\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy')
	
	server.start()
	#server.create_proxy()
	proxy_server = server.create_proxy()

	proxyConfig = Client.webdriver_proxy(proxy_server)

	
	#write_log("Proxy port: " + proxyConfig)
	#write_log("Proxy port: " + proxyConfig.getHttpProxy())

	opt = Options()
	opt.add_argument("--proxy-server={0}".format(proxy_server.proxy))
	opt.add_argument("--remote-allow-origins=*")
	#opt.add_argument("--headless=new")
	
	#options.setExperimentalOption("prefs", chromePrefs);
	#opt.set_capability(CapabilityType.ACCEPT_SSL_CERTS, proxyConfig)
	#opt.set_capability(CapabilityType.PROXY, proxyConfig)
	opt.add_extension("c:\\chromedriver\\1.2.8_0.crx")
	#opt.add_extension("c:\\chromedriver\\1.1_0.crx")
		
	#options.setProxy(proxyConfig);
	
			
	#driver = new ChromeDriver(options);

	
	drv = webdriver.Chrome(service=ChromeService('c:/chromedriver/chromedriver.exe'), options= opt)
	drv.get(startUrl)
	proxy_server.new_har()
	#print('zz')
	return {'drv' : drv, 'prx' : proxy_server}

	'''
	import net.lightbody.bmp.BrowserMobProxyServer;
	import net.lightbody.bmp.client.ClientUtil;
	import net.lightbody.bmp.core.har.Har;
	import net.lightbody.bmp.core.har.HarEntry;
	import net.lightbody.bmp.proxy.CaptureType;


	File cryp = new File("c:\\chromedriver\\1.2.8_0.crx");
	File crypsc = new File();
	if (windowsDebug) {
		System.setProperty("webdriver.chrome.driver", "c:\\chromedriver\\chromedriver.exe");
		} 
	else {
		System.setProperty("webdriver.chrome.driver", "/home/alexiv/Chromedriver/chromedriver");
		cryp = new File("/home/alexiv/Chromedriver/1.2.8_0.crx");
	}
		
	proxyServer = new BrowserMobProxyServer();
	proxyServer.setTrustAllServers(true);
	proxyServer.start();
	proxyServer.enableHarCaptureTypes(CaptureType.REQUEST_CONTENT, CaptureType.RESPONSE_CONTENT);
	proxyServer.newHar();
	Proxy proxyConfig = ClientUtil.createSeleniumProxy(proxyServer);
 
	writeLog("Proxy port: " + proxyConfig);
	writeLog("Proxy port: " + proxyConfig.getHttpProxy());
	try {
		if (jRBMIChrome.isSelected()) {
			Map<String, Object> chromePrefs = new HashMap<String, Object>();
			chromePrefs.put("profile.content_settings.exceptions.automatic_downloads.*.setting", 1 );
			
			++ChromeOptions options = new ChromeOptions();
			options.addArguments("--remote-allow-origins=*");
			options.setExperimentalOption("prefs", chromePrefs);
			options.setCapability(CapabilityType.ACCEPT_SSL_CERTS, proxyConfig);
			options.setCapability(CapabilityType.PROXY, proxyConfig);
			options.setProxy(proxyConfig);
			options.addExtensions(cryp);
			options.addExtensions(crypsc);
			
			driver = new ChromeDriver(options);

			if (saveLog) {
				EventFiringWebDriver eventFiringWebDriver = new EventFiringWebDriver(driver);
				eventFiringWebDriver.register(cll);
				driver = eventFiringWebDriver;
			}

		}
		js = (JavascriptExecutor) driver;

		if (driver == null) {
			writeLog("драйвер браузера не установлен.");
			return false;
		}
		driver.manage().timeouts().implicitlyWait(Duration.ofMillis(200));
		driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(10));
		driver.get(startUrl);
		driver.manage().deleteAllCookies();
	} 
	catch (Exception ex) {
		writeLog(ex.getMessage());
		writeLog(bName + "Ошибка доступа к стартовой странице");
		return false;
	}
	return true;

	'''




def elemAction(fName, eIdx, eCmd, eSnd, cmdNotReq):
	global driver
	cntRepeat = 0

	'''
	WebElement actEl;
	
	String fldTxt, varV;
	'''
	wait = WebDriverWait(driver, 0.5)


	# Ищем элементы без учета индекса
	zzw = driver.find_elements(By.XPATH, fName)
	
	if  len(zzw) == 0:
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

	print(eIdx)
	if eCmd == "click":
		wait.until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, fName)[eIdx])).click()
	elif eCmd == "dblclick":
		#(new Actions(driver)).doubleClick(wait.until(ExpectedConditions.elementToBeClickable(driver.findElements(fName).get(eIdx)))).perform();
		pass
	elif eCmd == "save":
		'''
		varV = driver.findElements(fName).get(eIdx).getAttribute("innerText");
				if (varV.isEmpty())
				{
					varV = driver.findElements(fName).get(eIdx).getAttribute("value");
				}
				addVarToArray(eSnd, varV);
		'''
		pass
	elif eCmd == "snd":
		if eSnd.startswith('Enter_'):
			#wait.until(ExpectedConditions.elementToBeClickable(driver.findElements(fName).get(eIdx))).sendKeys(eSnd.replace("Enter_", ""));
			#driver.findElements(fName).get(eIdx).sendKeys(Keys.ENTER);
			pass
		elif eSnd.startswith('Tab_'):
			#wait.until(ExpectedConditions.elementToBeClickable(driver.findElements(fName).get(eIdx))).sendKeys(eSnd.replace("Tab_", ""));
			#driver.findElements(fName).get(eIdx).sendKeys(Keys.TAB);
			pass
		elif eSnd.startswith('Clear_'):
			#actEl = driver.findElements(fName).get(eIdx);
			#actEl.click();
			#(new Actions(driver)).sendKeys(Keys.END).keyDown(Keys.SHIFT).sendKeys(Keys.HOME).keyUp(Keys.SHIFT).sendKeys(Keys.DELETE).perform();
			#wait.until(ExpectedConditions.elementToBeClickable(driver.findElements(fName).get(eIdx))).sendKeys(eSnd.replace("Clear_", ""));
			pass
		elif eSnd.startswith('JS_'):
			#js.executeScript("arguments[0].value='" + eSnd.replace("JS_", "") + "';", driver.findElements(fName).get(eIdx));
			#driver.findElements(fName).get(eIdx).sendKeys(Keys.TAB);
			pass
		else:
			wait.until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, fName)[eIdx])).send_keys(eSnd)
		while True:
			fldTxt = driver.find_elements(By.XPATH, fName)[eIdx].get_attribute("value")
			if fldTxt == eSnd or cntRepeat > 20: break
			time.sleep(0.1)
			cntRepeat += 1
	elif eCmd == "over":
		#new Actions(driver).moveToElement(driver.findElements(fName).get(eIdx)).perform();
		pass
	'''        
		try {

		} catch (Exception ex) {
			writeLog(ex.getMessage());
			return 6;
		}
	'''


# Выполнение шага теста
def sendCmdD(tStep):
	# +0 - команда выполнена
	# +3 - ошибка, но команда не обязательна
	# +4 - достигнута точка останова
	# +5 - команда пропущена
	# +6 - ошибка при поиске или выполнении действия над элементом
	# +9 - открыли адрес
	#String v_val, v_fnd, v_cmd, v_tst = "", cmp_val = "";
	#String menu_root, menu_sub, turl;
	#String s_txt, nc_s_txt, s_act, n_xpath = "", ns_xpath, css_search_window, css_res_window;
	#int elemIndex, waitTime, actionRes = 0, cntRep;
	toLog = ""
	cmdNotRequired = "notrequired" in tStep
	#simpleSelType = true
	#Wait<WebDriver> wait;
	#Wait<WebDriver> selWait;
	#WebElement tEl;
	#List<WebElement> tstArr;
	#String timeMask;
	global numReplay
	global driver

	
	s_act = tStep["action"] if "action" in tStep else ""

	if s_act == "Пауза": return 4
	if s_act == "Пропустить": return 5
	
	if "get" in tStep: # Открываем стартовую страницу
		turl = selTarget(tStep["get"])
		prepTest(turl)
		toLog = "Открытие адреса " + turl
	elif str(tStep["fnd"]).strip() == "@ЖдатьДо": # ждем наступления времени
		pass

	else:
		#wait = new WebDriverWait(driver, Duration.ofSeconds(1), Duration.ofMillis(200));
		#selWait = new WebDriverWait(driver, Duration.ofSeconds(10), Duration.ofMillis(200));
			
		v_val = str(tStep["val"]).strip()
		v_fnd = str(tStep["fnd"]).strip()
		v_cmd = str(tStep["cmd"]).strip() if "cmd" in tStep else "click"
		nc_s_txt = str(tStep["key"]).strip() if "key" in tStep else ""
		s_txt = prepSendKeys(nc_s_txt); # Предобработка ввода
		toLog = str(tStep["rem"]).strip() if "rem" in tStep else ""
		elemIndex = int(tStep["idx"]) if "idx" in tStep else -1

		# Пауза перед выполнением команды
		waitTime = int(tStep["wait"]) if "wait" in tStep else 0
			
		# Пропускаем команды со своим ожиданием, перед остальными выполняем задержку
		if not (v_fnd.startswith("@Недост") or v_fnd.startswith("@Доступ") or v_fnd.startswith("@Значение")):
			time.sleep(waitTime)


		# Если ЭОТТС - ждем недоступности элемента "Загрузка"
		#if (jRBMIEotts239.isSelected()) { waitLoadEotts(false, ""); }
		
		if v_fnd == "xpath":
			actionRes = elemAction(v_val.replace("[replay]", numReplay), elemIndex, v_cmd, s_txt, cmdNotRequired)
		elif v_fnd == "@СоздатьПТС":
			try:
				create_pts(s_txt)
				return 6
			except Exception as err:
				write_log(toLog + "... Ошибка")
				write_log(err)
				return 0
		
	return 9

# Ожидание выполнения запросов, путем анализа пакетов, прошедших прокси-сервер
def waitEndAjaxP(waitTimeSec, printLog, rem):
	if proxy_server == None: return
	curCnt = 0
	while True:
		curCnt = proxy_server.get_har
		print(zz)
		#currCnt = proxyServer.getHar().getLog().getEntries().size()
'''

	private void waitEndAjaxP(int waitTimeSec, Boolean printLog, String rem) {
	
		int stQ, sum0, sumErr, prevCnt = 0, currCnt=0;
		int cntRep = 0; 
		long startW, endW, qwrD;
		//startW = new Date().getTime();
		String strLog = "";
		Har httpMessages ;
		startW = new Date().getTime();
	
		do {
			try {
				Thread.sleep(250);
				
			} catch (Exception ex) {
			}
			
			currCnt = proxyServer.getHar().getLog().getEntries().size();
			
			cntRep++;
			if (currCnt > prevCnt) {
				prevCnt = currCnt;
				cntRep = 0;
			}
		} while  (cntRep < 4);
		
		sum0 = currCnt = sumErr = 0;
		httpMessages = proxyServer.getHar();
		for (HarEntry httpMessage : httpMessages.getLog().getEntries()) {
			if (httpMessage.getServerIPAddress().startsWith("10.")
					|| httpMessage.getServerIPAddress().startsWith("192.168.")) {
				stQ = httpMessage.getResponse().getStatus();
				currCnt++;
				if (stQ == 0) {
					sum0++;
				} else if (stQ == 200) {
					//sum200++;
				} else {
					sumErr++;
				}
			}
		}
		
		endW = new Date().getTime();
		qwrD =  (endW - startW) ;
		strLog = "Step: " + rem + "; XHR: " + currCnt + " (" + cntRep + ")" + "; Time: " + qwrD + "ms; No200: " + sumErr + "; NoResp: " + sum0;
		
		if (printLog) writeCon(strLog);
		if (proxyServer != null) proxyServer.newHar();
'''
# Выполнение команды
def old_send_сmd(tStep, num_stp, paamr, driver):
	# +0 - команда выполнена
	# +3 - ошибка, но команда не обязательна
	# +4 - достигнута точка останова
	# +5 - команда пропущена
	# +6 - ошибка при поиске или выполнении действия над элементом
	# +9 - открыли адрес
	#String v_val, v_fnd, v_cmd, v_tst = "", cmp_val = "";
	#String menu_root, menu_sub, turl;
	#String s_txt, nc_s_txt, s_act, n_xpath = "", ns_xpath, css_search_window, css_res_window;
	#int elemIndex, waitTime, actionRes = 0, cntRep;
	toLog = ""
	cmdNotRequired = "notrequired" in tStep
	#simpleSelType = true
	#Wait<WebDriver> wait;
	#Wait<WebDriver> selWait;
	#WebElement tEl;
	#List<WebElement> tstArr;
	#String timeMask;
	#global numReplay
	#global driver

	s_act = tStep["action"] if "action" in tStep else ""

	if s_act == "Пауза": return 4
	if s_act == "Пропустить": return 5
	
	if "get" in tStep: # Открываем стартовую страницу
		turl = selTarget(tStep["get"])
		driver = prepTest(turl)
		toLog = "Открытие адреса " + turl
	elif str(tStep["fnd"]).strip() == "@ЖдатьДо": # ждем наступления времени
		pass

	else:
		#wait = new WebDriverWait(driver, Duration.ofSeconds(1), Duration.ofMillis(200));
		#selWait = new WebDriverWait(driver, Duration.ofSeconds(10), Duration.ofMillis(200));
			
		v_val = str(tStep["val"]).strip()
		v_fnd = str(tStep["fnd"]).strip()
		v_cmd = str(tStep["cmd"]).strip() if "cmd" in tStep else "click"
		nc_s_txt = str(tStep["key"]).strip() if "key" in tStep else ""
		s_txt = prepSendKeys(nc_s_txt); # Предобработка ввода
		toLog = str(tStep["rem"]).strip() if "rem" in tStep else ""
		elemIndex = int(tStep["idx"]) if "idx" in tStep else -1

		# Пауза перед выполнением команды
		waitTime = int(tStep["wait"]) if "wait" in tStep else 0
			
		# Пропускаем команды со своим ожиданием, перед остальными выполняем задержку
		if not (v_fnd.startswith("@Недост") or v_fnd.startswith("@Доступ") or v_fnd.startswith("@Значение")):
			time.sleep(waitTime)


		# Если ЭОТТС - ждем недоступности элемента "Загрузка"
		#if (jRBMIEotts239.isSelected()) { waitLoadEotts(false, ""); }
		
		if v_fnd == "xpath":
			actionRes = elemAction(v_val.replace("[replay]", numReplay), elemIndex, v_cmd, s_txt, cmdNotRequired)
		elif v_fnd == "@СоздатьПТС":
			try:
				create_pts(s_txt)
				#return 6
				return 6, driver
			except Exception as err:
				write_log(toLog + "... Ошибка")
				write_log(err)
				#return 0
				return 0, driver
		
	return 9, driver

	