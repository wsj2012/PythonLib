# -*- coding:utf-8 -*-

import Logger
import requests
from bs4 import BeautifulSoup
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

def judgement_gender(class_name):
    if class_name == 'member_boy_ico':
        return '男'
    else:
        return '女'

def get_links(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'html.parser')
    links = soup.select('#page_list > ul > li > a')
    for link in links:
        href = link.get('href')
        get_info(href)

def get_info(href):
    wb_data = requests.get(href, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'html.parser')
    titles = soup.select('body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em')
    addresses = soup.select('body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p > span')
    prices = soup.select('#pricePart > div.day_l > span')
    imgs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')
    names = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    genders = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > span')

    for title, address, price, img, name, gender in zip(titles, addresses, prices,imgs, names, genders):
        data = {
            'title': title.get_text().strip(),
            'address': address.get_text().strip(),
            'price': price.get_text(),
            'img': img.get('src'),
            'name': name.get_text(),
            'gender': judgement_gender(gender.get('class'))
        }
        Logger.log(data)

if __name__ == '__main__':
    urls = ['http://sh.xiaozhu.com/search-duanzufang-p{}-0/'.format(number) for number in range(1, 3)]
    for single_url in urls:
        get_links(single_url)
        time.sleep(2)