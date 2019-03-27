
# -*- coding:utf-8 -*-
# import re

# phone = '123-4567-1234'
# new_phone = re.sub('\D', '', phone)
# print (new_phone)
# 12345671234

# a = 'one11two2three3'
# infos = re.search('\d+', a)
# print (infos.group())
# # 11
# infoss = re.findall('\d+', a)
# print (infoss)

# (.*?)表示()内的内容作为返回结果
# b = 'xxIxxjshdxxlovexxsffaxxpythonxx'
# r = re.findall('xx(.*?)xx', b)
# print (r)
# # ['I', 'love', 'python']

import urllib.request

import importlib,sys
importlib.reload(sys)
from bs4 import BeautifulSoup


# from lxml import etree
#
#

# etree = lxml.html.etree
# paser = etree.HTMLParser(encoding="utf-8")
# html = etree.parse('flower.html', parser=paser)
# result = etree.tostring(html, pretty_print=True)
# print (result)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'}
url = 'https://www.qiushibaike.com/text/'
# res = requests.get(url, headers=headers)
# selector = etree.HTML(res.text)
# html = etree.parse(res.text, paser=paser)
# resutl = etree.tostring(html, pretty_print=True)
# selector = etree.HTML(res.text)
# id = selector.xpath('//*[@id="qiushi_tag_121476924"]/div[1]/a[2]/h2/text()')[0]
# print (id)


def bs_scraper(url):
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req).read()

    # name = res.xpath('//*[@id="qiushi_tag_121466862"]/div[1]/a[2]/h2/text()')
    # print(name)

    soup = BeautifulSoup(res, 'html.parser')
    ids = soup.select('a > h2')
    contents = soup.select('div > span')
    laughs = soup.select('span.stats-vote > i')
    comments = soup.select('i.number')
    for id, content, laugh, comment in zip(ids, contents, laughs, comments):
        info = {
            'id': id.get_text(),
            'content': content.get_text(),
            'laugh': laugh.get_text(),
            'comment': comment.get_text()
        }
        print(info)

if __name__ == '__main__':
    urls = ['https://www.qiushibaike.com/text/page/{}/'.format(str(number) for number in range(1, 10))]
    for url in urls:
        bs_scraper(url)

