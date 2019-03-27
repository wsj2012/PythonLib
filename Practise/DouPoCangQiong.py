# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import re
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

f = open('/Users/wangshujun566/Desktop/doupo.txt', 'a+')

def get_info(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        contents = re.findall('<p>(.*?)</p>', res.content.decode('utf-8'), re.S)
        for content in contents:
            f.write(content+'\n')
    else:
        pass

if __name__ == '__main__':
    urls = ['http://www.doupoxs.com/doupocangqiong/{}.html'.format(number) for number in range(2, 10)]
    for url in urls:
        get_info(url)
        time.sleep(2)
f.close()