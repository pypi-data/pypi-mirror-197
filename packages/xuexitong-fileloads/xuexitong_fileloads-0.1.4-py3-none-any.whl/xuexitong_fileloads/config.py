


import json
import os
import sys

def app_path():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        return os.path.dirname(sys.executable)  #使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__)                 #没打包前的py目录
f_path=app_path()+r"\cookie.json"
headers = {
    'referer': 'https://mooc1.chaoxing.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}

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
