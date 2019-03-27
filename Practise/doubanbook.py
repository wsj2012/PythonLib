# -*- coding:utf-8 -*-

from lxml import etree
import requests
import re
from bs4 import BeautifulSoup
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

f = open('/Users/wangshujun566/Desktop/qiubai.txt', 'a+')


def get_info(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    ids = soup.select('div.author.clearfix > a > h2')
    contents = soup.select('a.contentHerf > div > span')
    for (id, content) in zip(ids, contents):
        print(id.get_text())
        print(content.get_text().strip())
        f.write(id.get_text().strip() + '\n')
        f.write(content.get_text().strip() + '\n\n')

    # selector = etree.HTML(res.text)
    # print(selector)
    # url_infos = selector.xpath('//div[@class="article block untagged mb15 typs_hot"]')
    # for url_info in url_infos:
    #     id = url_info.xpath('div[1]/a[2]/h2/text()')
    # # name = selector.xpath('//*[@id="qiushi_tag_121454622"]/div[1]/a[2]/h2/text()')[0]
    #     print(id)


if __name__ == '__main__':
    urls = ['https://www.qiushibaike.com/text/page/{}/'.format(str(number)) for number in range(0, 10)]
    for url in urls:
        get_info(url)
f.close()