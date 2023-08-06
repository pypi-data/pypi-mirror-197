


import json

import time

from bs4 import BeautifulSoup
import requests




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
        'referer':'https://mooc1.chaoxing.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}
    response = requests.get(url, headers=headers)
    # print(response)
    home_page = response.content
    if pab == 0:
        return home_page
    else:
        return home_page.decode()

def load_chapter_link(path_file):
    with open(path_file, 'r', encoding='utf-8') as fp:
        return json.loads(fp.read())

def js_html(browser,path, url, pab=2):
    if pab == 0:
        with open(path + 'html.txt', 'r', encoding='utf-8') as fp:
            return fp.read()
    if pab == 2:
        browser.get(url)
        time.sleep(5)
        save_data(browser.page_source, path + 'html.txt')
        return browser.page_source

