# -*- coding:utf-8 -*-

import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

info_lists = []

def judgement_gender(class_name):
    if class_name == 'womenIcon':
        return  '女'
    else:
        return '男'

def get_info(url):
    res = requests.get(url)
    ids = re.findall('<h2>(.*?)</h2>', res.text, re.S)
    levels = re.findall('<div class="articleGender \D+Icon">(.*?)</div>', res.text, re.S)
    genders = re.findall('<div class="articleGender (.*?)">', res.text, re.S)
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>', res.text, re.S)
    laughs = re.findall('<span class="stats-vote"><i class="number">(\d+)</i>', res.text, re.S)
    comments = re.findall('<i class="number">(\d+)</i>', res.text, re.S)

    for id, level, gender, content, laugh, comment in zip(ids, levels, genders, contents, laughs, comments):
        info = {
            'id': id,
            'level': level,
            'gender': judgement_gender(gender),
            'content': content,
            'laugh': laugh,
            'comment': comment
        }
        info_lists.append(info)

if __name__ == '__main__':
    urls = ['https://www.qiushibaike.com/text/page/{}/'.format(str(number)) for number in range(1, 10)]
    for url in urls:
        get_info(url)
    for info_list in info_lists:
        f = open('/Users/wangshujun566/Desktop/qiubai.txt', 'a+')
        try:
            f.write(info_list['id'] + '\n')
            f.write(info_list['level'] + '\n')
            f.write(info_list['gender'] + '\n')
            f.write(info_list['content'] + '\n')
            f.write(info_list['laugh'] + '\n')
            f.write(info_list['comment'] + '\n\n')
            f.close()
        except UnicodeEncodeError:
            pass