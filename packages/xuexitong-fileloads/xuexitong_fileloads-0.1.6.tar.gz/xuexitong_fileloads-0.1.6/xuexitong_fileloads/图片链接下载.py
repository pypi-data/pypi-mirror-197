# 敬启:今天也要好好的哦
# 来自:我的可爱们，刻晴，可莉等
# 时间:2022/1/18 23:08
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

def get_img_str(dir_img):
    with open(dir_img, 'r', encoding='utf-8') as fp:
        return fp.read()


def parse_img(img_str):
    # re.findall(r'<span class="zt_style"><img class="zt" src="(http.*?webp)"', img_str, re.DOTALL)
    html = BeautifulSoup(img_str, 'lxml')
    img_list = html.find_all('img', style="width:100%;")
    return img_list


# style="width:820px; margin:0 auto;padding: 40px 0;"
def load_img(dir_img='img_data\图片\\', img_list=[]):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'}
    # print(img_list)
    i = 1
    for img in tqdm(img_list, '图片下载中'):
        # print(len(img['src']))
        response = requests.get(img['src'],headers=headers)
        img_content = response.content
        with open(dir_img + str(i) + '.png', 'wb') as fp:
            fp.write(img_content)
        i += 1

def main(dir='图片\\'):
    img_str = get_img_str('食品化学.html')
    img_list = parse_img(img_str)
    load_img(dir, img_list)
