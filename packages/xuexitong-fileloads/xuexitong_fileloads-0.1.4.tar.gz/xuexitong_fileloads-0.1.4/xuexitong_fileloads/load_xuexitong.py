# 敬启:今天也要好好的哦
# 来自:我的可爱们，刻晴，可莉等
# 时间:2022/1/21 16:26
import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup
from utils import require,save_data,parsed_url,js_html
from config import headers



def load_file(basedir,src='', file_class=1):
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


def get_img_pdf(browser,basedir, url, start_inPage=0, end_inPage=3, file_class=1):
    '''02'''
    if start_inPage<0:
        start_inPage=0
    if end_inPage <= 0:
        end_inPage=1
    js_html_str = js_html(browser,basedir, url)
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
        file_html_str = js_html(browser,basedir, url=file_url, pab=2)
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
                load_file(basedir,src, file_class)
            except Exception as res:
                print('get_img_pdf,load_file抛出')
                print(res)
        i += 1


def load_loop(browser,basedir, chapter_link_list:list,start_chapter=0, end_chapter=0, file_class=1,start_inPage = 0,end_inPage = 1):
    if start_chapter<0:
        start_chapter=0
    if end_chapter <= 0:
        len_chapter = len(chapter_link_list)
        end_chapter=len_chapter
    else:
        len_chapter = end_chapter - start_chapter

    count = 1
    for url in chapter_link_list[start_chapter:end_chapter]:
        print('爬取中...%d/%d' % (count, len_chapter))
        time.sleep(0.5)
        try:
            get_img_pdf(browser,basedir, url, start_inPage, end_inPage, file_class)
        except Exception as result:
            print("load_loop",result)
        count += 1


def get_all_chapter_link(browser,basedir, url,close_browser = 0):
    js_html_str = js_html(browser,basedir, url)
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
        # url = baseurl + src + '&enc=5ba8e9a7c6fd69e07d767c81e94816de&mooc2=1'
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


