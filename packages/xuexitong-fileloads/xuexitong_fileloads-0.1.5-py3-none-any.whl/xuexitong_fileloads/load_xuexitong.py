# 敬启:今天也要好好的哦
# 来自:我的可爱们，刻晴，可莉等
# 时间:2022/1/21 16:26
import os
import json
import re
import sys
import time
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

headers = {
    'referer': 'https://mooc1.chaoxing.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}

def parsed_url(html_str=''):
    # re.findall(r'<span class="zt_style"><img class="zt" src="(http.*?webp)"', img_str, re.DOTALL)
    html = BeautifulSoup(html_str, 'lxml')
    iframe = html.find('iframe', id="iframe")
    src = iframe['src']
    url = 'https://mooc1.chaoxing.com' + src
    return url


def save_data(home_page, path_file='', w='w'):
    if 'b' in w:
        with open(path_file, w) as fp:
            fp.write(home_page)
        return
    with open(path_file, w, encoding='utf-8') as fp:
        fp.write(home_page)


def require(url='', pab=0):
    headers = {
        'referer': 'https://mooc1.chaoxing.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}
    response = requests.get(url, headers=headers)
    # print(response)
    home_page = response.content
    if pab == 0:
        return home_page
    else:
        return home_page.decode()


def load_file(src='', file_class=1):
    # chapter ='第'+ str(num)+'章'
    response = requests.get(src, headers=headers)
    print(response)
    # print(response)
    file = response.content.decode()
    data = json.loads(file)
    # save_data(data['filename'] + '\n', basedir + 'file_url.txt.txt', w='a')

    filename = data['filename'].replace('.mp4', '')
    print(filename)
    if file_class == 3:
        if data.get('mp3', '0') == '0':
            pass
        else:
            url_mp3 = data['download']
            save_data(require(url=url_mp3), path_file=basedir + filename + '.mp3', w='wb')
            url_mp4 = data['http']
            save_data(require(url=url_mp4), path_file=basedir + filename + '.mp4', w='wb')
            return
        if data.get('pdf', '0') == '0':
            pass
        else:
            url_pdf = data['pdf']
            save_data(require(url=url_pdf), path_file=basedir + filename, w='wb')
            return
    elif file_class == 2:
            if data.get('pdf', '0') == '0':
                pass
            else:
                url_pdf = data['pdf']
                filename = filename.replace('pptx', 'pdf')
                filename=filename.replace('ppt', 'pdf')
                filename = filename.replace('docx', 'pdf')
                filename = filename.replace('doc', 'pdf')
                save_data(require(url=url_pdf), path_file=basedir + filename, w='wb')
                return
    elif file_class==1:
        if data.get('mp3', '0') == '0':
            pass
        else:
            url_mp4 = data['http']
            save_data(require(url=url_mp4), path_file=basedir + filename + '.mp4', w='wb')
            return
    else:
        return


def get_img_pdf(basedir, url, start_inPage=0, end_inPage=3, file_class=1):
    '''02'''
    if start_inPage<0:
        start_inPage=0
    if end_inPage <= 0:
        end_inPage=1
    js_html_str = js_html(basedir, url)
    file_url = parsed_url(js_html_str)
    # file_url=file_url.replace('num=0','num=1')
    save_data(file_url + '\n', basedir + 'card_url.txt', w='a')
    # flag为统计十次内第二页空值情况，>1则置页内循环次数num为1,似乎有bug已删
    i = start_inPage
    print(end_inPage)
    while i <= end_inPage:
        # url_num=re.findall('num=(\d{1,3})',file_url)[0]
        url_num = re.findall('num=(\d)', file_url)
        if len(url_num) == 0:
            file_url += '&num={}'.format(i)
        else:
            file_url = file_url.replace('num=' + url_num[0], 'num=' + str(i))
        print(file_url)
        print(i)
        file_html_str = js_html(basedir, url=file_url, pab=2)
        # print(file_html_str)
        # 处理空值异常处
        file_json_str0 = re.findall(r'mArg =.*?"attachments":(.*?}]),"', file_html_str)
        n = len(file_json_str0)
        if n == 0:
            print('inPage_num=' + str(i) + '无匹配值，请开发者自行查看')
            i+=1
            continue
        print(file_json_str0)
        file_json_str = file_json_str0[0]
        # if len(file_json_str ) == 0:
        #     return
        file_json = json.loads(file_json_str)
        for file_json_each in file_json:
            try:
                src = 'https://mooc1.chaoxing.com/ananas/status/' + file_json_each['property']['objectid']
            except Exception as result:
                print('get_img_pdf,objectid取值失败，小概率事件(单元测验),pass')
                print(result)
                continue
            if file_json_each['property'].get('name'):
                name = file_json_each['property'].get('name')
            else:
                name = ''
            save_data(src + ',' + name + '\n', basedir + 'file_url.txt', w='a')
            
            print(src)
            if file_class==0:
                continue
            try:
                load_file(src, file_class)
            except Exception as res:
                print('get_img_pdf,load_file抛出')
                print(res)
        i += 1


def load_chapter_link(path_file):
    with open(path_file, 'r', encoding='utf-8') as fp:
        return json.loads(fp.read())

def load_loop(chapter_link_list:list,start_chapter=0, end_chapter=0,start_inPage = 0,end_inPage = 1, file_class=1):
    if start_chapter<0:
        start_chapter=0
    if end_chapter <= 0:
        len_chapter = len(chapter_link_list)
        end_chapter=len_chapter
    else:
        len_chapter = end_chapter - start_chapter
    #大于2，循环自减删除
    # while start_chapter >= 1:
    #     del chapter_link_list[start_chapter - 1]
    #     start_chapter -= 1
    count = 1
    for url in chapter_link_list[start_chapter:end_chapter]:
        print('爬取中...%d/%d' % (count, len_chapter))
        time.sleep(0.5)
        try:
            get_img_pdf(basedir, url, start_inPage, end_inPage, file_class)
        except Exception as result:
            print("load_loop",result)
        count += 1

def js_html(path, url, pab=2):
    if pab == 0:
        with open(path + 'html.txt', 'r', encoding='utf-8') as fp:
            return fp.read()
    if pab == 2:
        browser.get(url)
        time.sleep(5)
        save_data(browser.page_source, path + 'html.txt')
        return browser.page_source
# def addCookie():
#     cookies='lv=1;'
    
#     for item in cookies.split("; "):
#         cookiedict={} 
#         item.split("=")
#         cookiedict["name"]=item[0]
#         cookiedict["value"]=item[1]
#         cookiedict['path']='/'
#         browser.add_cookie(cookiedict)

def get_all_chapter_link(basedir, url,close_browser = 0):
    js_html_str = js_html(basedir, url)
    # print(js_html_str)
    chapterId_html = BeautifulSoup(js_html_str, 'lxml')
    chapterId_tag_list = chapterId_html.find_all('span', class_="posCatalog_name")
    save_data(str(browser.page_source), basedir + 'html.txt')
    chapterId_list = []

    print(chapterId_tag_list)
    #章节tag列表
    for chapterId_tag in chapterId_tag_list:
        try:
            x = chapterId_tag['onclick']
        except:
            print(chapterId_tag['title'] + '已锁定，爬取失败')
            continue
        chapterId_unit = re.findall(r"'(.*?)'", x)
        if len(chapterId_unit) == 3:
            chapterId_list.append(chapterId_unit)
            #getTeacherAjax('227','6103','630');
        # 312
    baseurl = 'https://mooc1.chaoxing.com/mycourse/studentstudy'
    chapter_url_list = []
    enc=re.findall('&enc=.*?&mooc2=1',url)[0]
    #章节tagid列表,构建url
    for chapterId in chapterId_list:
        src = '?chapterId=' + chapterId[2] + '&courseId=' + chapterId[0] + '&clazzid=' + chapterId[1]
        # url = baseurl + src + '&enc=&mooc2=1'
        url = baseurl + src + enc
        chapter_url_list.append(url)

    save_data(json.dumps(chapter_url_list,ensure_ascii=False), path_file=basedir + 'chapter_link.json', w='w')

    i = 0
    j = 0
    chapterId_dict = {}
    #章节tag列表,构建章节url字典，不参与程序
    for chapterId_tag in chapterId_tag_list:
        try:
            x = chapterId_tag['onclick']
            chapterId_dict[chapterId_tag['title']]=chapter_url_list[i]
            i += 1
        except KeyError:
            try:
                chapterId_dict[chapterId_tag['title']]=''
            except KeyError:
                pass
        j += 1
    print("爬取成功%d个，失败%d个，原应爬取%d个" % (i, j - i, j))
    save_data(json.dumps(chapterId_dict,ensure_ascii=False), path_file=basedir + '全部章节链接.json', w='w')
    if close_browser == 1:
        browser.quit()

def selenium_set():
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

def cookies_login(url,exe=False):
    """
    Cookies登录方法
    :param cookies: 网页所需要添加的Cookie
    """
    
    browser.get(url)
    if exe and "passport" not in browser.current_url[:16]:
        return
    cookies=load_cookies(encoding="utf-8")
    if cookies!={}:
        browser.delete_all_cookies()
        current_url=browser.current_url
        print(browser.current_url)
        index=browser.current_url.find('?')
        if index!=-1:
            current_url=current_url[:index]
        index=browser.current_url.rfind('/')
        if index!=-1:
            current_url=current_url[:index]
        current_url_len=len(current_url)
        print(current_url)
        for c in cookies:
            domain=c["domain"]
            domain_len=len(domain)
            if domain_len>current_url_len or domain not in current_url[current_url_len-domain_len:]:
                print(domain,current_url[current_url_len-domain_len:])
                continue
            browser.add_cookie(c)
        browser.get(url)
        time.sleep(1.5)
        browser.refresh()
        if "passport" in browser.current_url[:16]:
            print('cookie失效')
            input('请扫码登录继续,然后输入*并回车继续,如有第二次请忽略并再次输入:')
            time.sleep(1)
            save_cookies(browser.get_cookies())
    else:
        input('请扫码登录继续,然后输入*并回车继续,如有第二次请忽略并再次输入:')
        time.sleep(1)
        save_cookies(browser.get_cookies())

def app_path():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        return os.path.dirname(sys.executable)  #使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__)                 #没打包前的py目录

def input_inPage_num(config_dict:dict,):
    if '0' in mode_op:
        file_class = int(input('输入循环下载类型2全部1pdf0mp4:'))
        start_inPage = int(input('节内页始0：'))
        end_inPage = int(input('节内页终1：'))
    else:
        file_class = config_dict['file_class']
        start_inPage=config_dict['start_inPage']
        end_inPage = config_dict['end_inPage']
    return file_class,start_inPage,end_inPage
if __name__ == '__main__':
    print("可以在配置文件中输入参数：")
    f_path=app_path()+r"\cookie.json"
    config_path=app_path()+"/config.json"
    if not os.path.exists(config_path):
        config_dict={"basedir":"学习通资料图片\\课程名\\音频\\","url":"","loop_op":"2","mode_op":"9",
                     "file_class":"1","start_inPage":"0","end_inPage":"1","start_chapter":"0","end_chapter":"0",
    "help":"mode_op 模式选择9自定义,0极简.loop_op 按2自动循环1手动单次.file_class 输入循环下载类型3全部2pdf1mp4不下载0,start_inPage章节内页面"
    }
        with open(config_path,'w',encoding='utf-8') as fp:
            fp.write(config_dict)

    with open(config_path,'r',encoding='utf-8') as fp:
        config_dict=json.loads(fp.read())
    next = '9'
    exe=False
    browser = selenium_set()
    while '0' not in next:
        try:
            if config_dict['mode_op']=="":
                mode_op = input('模式选择9自定义,0极简:')
            else:
                mode_op=config_dict['mode_op']
                print("模式选择{}".format(mode_op))
            if '9' in mode_op or ('0' not in mode_op and exe):
                basedir = input('基本目录:')
                url = input('url:')
                loop_op = input('按2自动循环1手动单次:')
            else:
                basedir = config_dict['basedir']
                url = config_dict['url']
                loop_op = config_dict['loop_op']
                print(basedir,url,loop_op)
            if not os.path.isabs(basedir):
                basedir=app_path()+'/'+basedir
            if basedir[-1:] not in ['\\','/']:
                basedir+='/'
            if not os.path.isdir(basedir):
                os.makedirs(basedir)
            save_data('----------\n', basedir + 'file_url.txt', w='a')
            save_data('----------\n', basedir + 'card_url.txt', w='a')
            # count = 0
            print("cookies登录")
            cookies_login(url,exe)
            exe=True
            if '9' in mode_op:
                file_class = int(input('输入循环下载类型3全部2pdf1mp4不下载0:'))
                start_inPage = int(input('节内页始于0：'))
                end_inPage = int(input('节内页终于数据：'))
            else:
                file_class = int(config_dict['file_class'])
                start_inPage=int(config_dict['start_inPage'])
                end_inPage = int(config_dict['end_inPage'])
            if '2' in loop_op:
                if '9' in mode_op:
                    start_chapter = int(input('输入循环开始章节,从1计数:'))
                    end_chapter = int(input('输入循环结束章节,从1计数,不设定则输入0:'))
                else:
                    start_chapter = int(config_dict['start_chapter'])
                    end_chapter = int(config_dict['end_chapter'])
                print('获取各章链接中...')
                get_all_chapter_link(basedir, url)
                chapter_link_list = load_chapter_link(basedir + 'chapter_link.json')
                load_loop(chapter_link_list,start_chapter-1, end_chapter,file_class,start_inPage, end_inPage)
            else:
                isNext = '1'
                while True:
                    get_img_pdf(basedir, url, start_inPage, end_inPage,file_class)
                    isNext = input('全输入继续2 url输入继续1 离开0:')
                    if '0' not in isNext:
                        break
                    url = input('所要下载资源所在页面url:')
                    if '1' in isNext:
                        file_class = int(input('输入循环下载类型3全部2pdf1mp4不下载0:'))
                        start_inPage=int(input('节内页始0：'))
                        end_inPage = int(input('节内页终2：'))
            
        except ValueError as result:
            input('ValueError:', result, '\n请重新输入,顶层代码附上\n回车继续')



