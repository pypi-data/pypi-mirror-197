import os
import json
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config import f_path

def selenium_set()->webdriver.Chrome:
    print('正在唤起谷歌浏览器,唤起后请勿关闭，手动最小化即可...')
    time.sleep(1)
    # 进入浏览器设置
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('-ignore-certificate-errors')
    options.add_argument('-ignore -ssl-errors')
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 设置中文
    options.add_argument('lang=zh_CN.UTF-8')
    
    # 更换头部
    
    options.add_argument('content-type="application/x-www-form-urlencoded"')
    # 创建浏览器对象
    # accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    s = Service('C:\Program Files\Google\Chrome\Application\chrome.exe')
    browser = webdriver.Chrome(options=options)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    return browser

def save_cookies(data, encoding="utf-8"):
    """
    Cookies保存方法
    :param data: 所保存数据
    :param encoding: 文件编码,默认utf-8
    """
    with open(f_path, "w", encoding=encoding) as f_w:
        json.dump(data, f_w)

def load_cookies(encoding="utf-8"):
    """
    Cookies读取方法
    :param encoding: 文件编码,默认utf-8
    """
    if os.path.isfile(f_path):
        with open(f_path, "r", encoding=encoding) as f_r:
            user_status = json.load(f_r)
        return user_status
    else:
        return {}

def cookies_login(browser:webdriver.Chrome,url,exe=False):
    """
    Cookies登录方法
    :param cookies: 网页所需要添加的Cookie
    """
    browser.get(url)
    if exe and "passport" not in browser.current_url:
        return
    cookies=load_cookies(encoding="utf-8")
    if cookies!={}:
        browser.delete_all_cookies()
        print(browser.current_url)
        for c in cookies:
            domain=c["domain"]
            if ".chaoxing.com"!=domain:
                continue
            browser.add_cookie(c)
        browser.get(url)
        time.sleep(1.5)
        browser.refresh()
        if "passport" in browser.current_url:
            print('cookie失效')
            input('请扫码登录继续,然后输入*并回车继续,如有第二次请忽略并再次输入:')
            time.sleep(1)
            save_cookies(browser.get_cookies())
            # cookies_login(browser,url,exe)
    else:
        input('请扫码登录继续,然后输入*并回车继续,如有第二次请忽略并再次输入:')
        time.sleep(1)
        save_cookies(browser.get_cookies())
        # cookies_login(browser,url,exe)

def input_inPage_num(config_dict:dict,mode_op):
    if '0' in mode_op:
        file_class = int(input('输入循环下载类型2全部1pdf0mp4:'))
        start_inPage = int(input('节内页始0：'))
        end_inPage = int(input('节内页终1：'))
    else:
        file_class = config_dict['file_class']
        start_inPage=config_dict['start_inPage']
        end_inPage = config_dict['end_inPage']
    return file_class,start_inPage,end_inPage

