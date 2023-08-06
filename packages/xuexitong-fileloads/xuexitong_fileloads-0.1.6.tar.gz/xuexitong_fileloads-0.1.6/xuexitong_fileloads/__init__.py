



import os
from load_xuexitong import get_all_chapter_link, get_img_pdf, load_loop, save_data
from login import cookies_login, selenium_set
from utils import load_chapter_link
from config import config_dict,app_path,next

if __name__ == '__main__':
    exe=False
    browser = selenium_set()
    while '0' not in next:
        try:
            mode_op=config_dict['mode_op']
            if mode_op=="":
                mode_op = input('模式选择9自定义,0极简:')
            else:
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
            cookies_login(browser,url,exe)
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
                    end_chapter = int(input('输入循环结束章节,终于终数,不设定则输入0:'))
                else:
                    start_chapter = int(config_dict['start_chapter'])
                    end_chapter = int(config_dict['end_chapter'])
                print('获取各章链接中...')
                get_all_chapter_link(browser,basedir, url)
                chapter_link_list = load_chapter_link(basedir + 'chapter_link.json')
                load_loop(browser,basedir, chapter_link_list,start_chapter-1, end_chapter,start_inPage, end_inPage,file_class)
            else:
                isNext = '1'
                while True:
                    get_img_pdf(browser,basedir, url, start_inPage, end_inPage,file_class)
                    isNext = input('全输入继续2 url输入继续1 离开0:')
                    if '0' not in isNext:
                        break
                    url = input('所要下载资源所在页面url:')
                    if '1' in isNext:
                        file_class = int(input('输入循环下载类型3全部2pdf1mp4不下载0:'))
                        start_inPage=int(input('节内页始0：'))
                        end_inPage = int(input('节内页终,终于终数：'))
            
        except ValueError as result:
            input('ValueError: invalid literal for int() with base 10','\n,非法配置，请重新输入配置数字请,顶层代码附上\n回车重新加载')



