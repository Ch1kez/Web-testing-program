import datetime
import time

import psutil
from browsermobproxy import Client
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .fnFTA import *


# Подготовка драйвера и прокси для теста
def prep_test(t_info):
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == "browsermob-proxy":
            proc.kill()

    server = Server(t_info['tst_par']['bmp_path'], options={'port': 9091})

    server.start()
    proxy_server = server.create_proxy()
    proxyConfig = Client.webdriver_proxy(proxy_server)

    opt = Options()
    opt.add_argument("--proxy-server={0}".format(proxy_server.proxy))
    opt.add_argument("--remote-allow-origins=*")
    # opt.add_argument("--headless=new")

    opt.add_extension("c:\\chromedriver\\1.2.8_0.crx")
    # opt.add_extension("c:\\chromedriver\\1.1_0.crx")

    drv = webdriver.Chrome(service=ChromeService(t_info['tst_par']['drv_path']), options=opt)
    turl = t_info['tst_par']['tadr']
    drv.get(turl)
    proxy_server.new_har()
    t_info['drv'] = drv
    t_info['prx'] = proxy_server
    # t_info['log_arr'][t_info['cur_step']] =
    return "Открытие адреса " + turl


def elem_action(tst_info, fName, eIdx, eCmd, eSnd, cmdNotReq):
    driver = tst_info['drv']
    cntRepeat = 0

    '''
    WebElement actEl;
    
    String fldTxt, varV;
    '''
    wait = WebDriverWait(driver, 0.5)

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
        # (new Actions(driver)).doubleClick(wait.until(ExpectedConditions.elementToBeClickable(driver.findElements(fName).get(eIdx)))).perform();
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
            # wait.until(ExpectedConditions.elementToBeClickable(driver.findElements(fName).get(eIdx))).sendKeys(eSnd.replace("Enter_", ""));
            # driver.findElements(fName).get(eIdx).sendKeys(Keys.ENTER);
            pass
        elif eSnd.startswith('Tab_'):
            # wait.until(ExpectedConditions.elementToBeClickable(driver.findElements(fName).get(eIdx))).sendKeys(eSnd.replace("Tab_", ""));
            # driver.findElements(fName).get(eIdx).sendKeys(Keys.TAB);
            pass
        elif eSnd.startswith('Clear_'):
            # actEl = driver.findElements(fName).get(eIdx);
            # actEl.click();
            # (new Actions(driver)).sendKeys(Keys.END).keyDown(Keys.SHIFT).sendKeys(Keys.HOME).keyUp(Keys.SHIFT).sendKeys(Keys.DELETE).perform();
            # wait.until(ExpectedConditions.elementToBeClickable(driver.findElements(fName).get(eIdx))).sendKeys(eSnd.replace("Clear_", ""));
            pass
        elif eSnd.startswith('JS_'):
            # js.executeScript("arguments[0].value='" + eSnd.replace("JS_", "") + "';", driver.findElements(fName).get(eIdx));
            # driver.findElements(fName).get(eIdx).sendKeys(Keys.TAB);
            pass
        else:
            wait.until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, fName)[eIdx])).send_keys(eSnd)
        while True:
            fldTxt = driver.find_elements(By.XPATH, fName)[eIdx].get_attribute("value")
            if fldTxt == eSnd or cntRepeat > 20: break
            time.sleep(0.1)
            cntRepeat += 1
    elif eCmd == "over":
        # new Actions(driver).moveToElement(driver.findElements(fName).get(eIdx)).perform();
        pass
    '''        
        try {

        } catch (Exception ex) {
            writeLog(ex.getMessage());
            return 6;
        }
    '''


# Выполнение команды теста
def send_сmd(t_info):
    numReplay = '0'
    t_step = t_info['cur_cmd']
    tst_sep = t_info["t_info"]['tst_par']['tsts'].startswith('СЭП')
    to_log = ""
    use_proxy = False
    cmdNotRequired = "notrequired" in t_step

    v_fnd = str(t_step['fnd']).strip() if 'fnd' in t_step else ''

    if v_fnd != '@xpathNoProxy' and t_info["t_info"]['prx'] != None:
        t_info["t_info"]['prx'].new_har()
        use_proxy = True
    elif v_fnd == '@xpathNoProxy':
        v_fnd = 'xpath'
    # -----------------------------------------------
    if "get" in t_step:  # Открываем стартовую страницу
        to_log = prep_test(t_info["t_info"])
    # elif v_fnd == "@ЖдатьДо": # Не реализовано. ждем наступления времени
    #	pass
    else:

        v_val = str(t_step['val']).strip() if 'val' in t_step else ''
        v_cmd = str(t_step['cmd']).strip() if 'cmd' in t_step else 'click'
        nc_s_txt = str(t_step['key']).strip() if 'key' in t_step else ''
        s_txt = prep_send_keys(nc_s_txt, t_info["t_info"])  # Предобработка ввода
        to_log = str(t_step['rem']).strip() if 'rem' in t_step else ''
        elem_idx = int(t_step['idx']) if 'idx' in t_step else -1

        # Пауза перед выполнением команды
        wait_time = int(t_step["wait"]) if "wait" in t_step else 0

        # Пропускаем команды со своим ожиданием, перед остальными выполняем задержку
        if not (v_fnd.startswith("@Недост") or v_fnd.startswith("@Доступ") or v_fnd.startswith("@Значение")):
            if wait_time != 0:
                time.sleep(wait_time)

        # Если ЭОТТС - ждем недоступности элемента "Загрузка"
        # if (jRBMIEotts239.isSelected()) { waitLoadEotts(false, ""); }

        if v_fnd == "xpath":
            actionRes = elem_action(t_info["t_info"], v_val.replace("[replay]", numReplay), elem_idx, v_cmd, s_txt,
                                    cmdNotRequired)
        elif v_fnd == "@СоздатьПТС":
            try:
                create_pts(t_info["t_info"], s_txt)
                return 6
            except Exception as err:
                write_log(to_log + "... Ошибка")
                write_log(err)
                return 0
        # ---------------------------------------------------------------------------
        if v_fnd == '@xpathNoProxy':
            time.sleep(wait_time)
        elif t_info["t_info"]['prx'] != None:
            wait_end_ajax(t_info["t_info"], 2, t_info["t_info"]['cur_step'])
            if tst_sep:
                wait_load_sep(t_info["t_info"]['drv'])
            else:
                wait_load_eotts(False, "")

    # Запись в массив лога
    t_info["t_info"]['log_arr'][t_info["t_info"]['cur_step']] = to_log


# Ожидание выполнения запросов, путем анализа пакетов, прошедших прокси-сервер
def wait_end_ajax(tst_inf, waitTimeSec, rem):
    bmp_prx = tst_inf['prx']
    prevCnt = 0
    currCnt = 0
    cntRep = 0

    startW = datetime.datetime.now()

    while True:
        time.sleep(0.25)

        currCnt = len(bmp_prx.har['log']['entries'])
        cntRep += 1
        if currCnt > prevCnt:
            prevCnt = currCnt
            cntRep = 0
        if cntRep > 3:
            break
    sum0 = 0
    currCnt = 0
    sumErr = 0
    httpMessages = bmp_prx.har['log']['entries']
    for h in httpMessages:
        if str(h['serverIPAddress']).startswith('10.') or str(h['serverIPAddress']).startswith('192.168.'):
            currCnt += 1
            stQ = h['response']['status']  # ttpMessage.getResponse().getStatus()
            if stQ == 0:
                sum0 += 1
            elif stQ == 200:
                pass
            else:
                sumErr += 1
    endW = datetime.datetime.now()
    qwrD = endW - startW
    dlt = int(qwrD.microseconds / 1000)
    strLog = "XHR: {0} ({1}); Time: {2} ms; No200: {3}; NoResp: {4};".format(currCnt, cntRep, dlt, sumErr, sum0)
    tst_inf['log_ajax'][rem] = strLog
    print(strLog)


# Ожидание загрузки в СЭП
def wait_load_sep(driver):
    cntRep = 0
    n_xpath = "//div[contains(@class, 'loader')][contains(@class, 'active')]"
    while True:
        zz = driver.find_elements(By.XPATH, n_xpath)
        if len(zz) == 0:
            break
        elif not zz[0].is_displayed() or not zz[0].is_enabled():
            break
        elif cntRep > 1200:
            # writeLog( "... Загрузка больше 2 мин.")
            break
        time.sleep(0.1)
        cntRep += 1


def wait_load_eotts():
    '''
    '''
    pass
