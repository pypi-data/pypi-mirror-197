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

int('p')