import os
from pprint import pprint

import requests


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

# a=require('https://mooc1.chaoxing.com/ananas/status/e2115c0d7229e2bfdd0cb1c7391ad0f0',1)
# pprint(a)
# with open('path_file.json', 'w', encoding='utf-8') as fp:
#     fp.write(a)
# a='19/'
# print(a[-1:])
# print(os.path.isabs('c:/'))

int('p')