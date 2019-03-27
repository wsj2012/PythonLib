# -*- coding:utf-8 -*-

import csv
import requests
from bs4 import BeautifulSoup

import xlwt

all_info_list = []


fp = open('/Users/wangshujun566/Desktop/douban.csv', 'w+', newline="", encoding='utf-8')
writer = csv.writer(fp)
writer.writerow(('name', 'url', 'author', 'publisher', 'date', 'price', 'rate', 'comment'))

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

def get_info(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    names = soup.select('td > div.pl2 > a')
    links = soup.find_all('div', class_="pl2")
    jjs = soup.select('tr > td > p.pl')
    book_infos = soup.select('tr > td > p.pl')
    rates = soup.select('tr > td > div.star.clearfix > span.rating_nums')
    comments = soup.select('tr > td > p.quote > span')
    for (name, jj, link, book_info, rate, comment) in zip(names, jjs, links, book_infos, rates, comments):
        bookname = name.get('title')
        href = link.find_all('a')[0].get('href')
        info = book_info.get_text().strip()
        author = info.split('/')[0].strip()
        publisher = info.split('/')[-3].strip()
        date = info.split('/')[-2].strip()
        price = info.split('/')[-1].strip()
        rat = rate.get_text().strip()
        comm = comment.get_text().strip()
        writer.writerow((bookname, href, author, publisher, date, price, rat, comm))
        info_list = [bookname, href, author, publisher, date, price, rat, comm]
        all_info_list.append(info_list)

if __name__ == '__main__':
    ulrs = ["https://book.douban.com/top250?start={}".format(str(number)) for number in range(0, 250, 25)]
    for url in ulrs:
        get_info(url)

    header = ['book name', 'line', 'auhtor', ' publisher', 'date', 'price', 'reate', 'comment']
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Sheet1')
    for h in range(len(header)):
        sheet.write(0, h, header[h])
    i = 1
    for list in all_info_list:
        j = 0
        for data in list:
            sheet.write(i, j, data)
            j += 1
        i += 1

book.save('/Users/wangshujun566/Desktop/doubanTop.xls')
fp.close()
