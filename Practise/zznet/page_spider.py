import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo

client = pymongo.MongoClient('localhost', 27017, connect=False)
mydb = client['mydb']
tongcheng_url = mydb['tongcheng_url']
tongcheng_info = mydb['tongcheng_info']

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'Connection': 'keep-alive'}


def get_links(channel, pages):

    list_view ='{}pn{}'.format(channel, str(pages))
    try:
        html = requests.get(list_view, headers=headers)
        time.sleep(2)
        soup = BeautifulSoup(html.text, 'html.parser')
        infos = soup.find_all('td', class_='t')

        for(info) in zip(infos):
            url = info[0].find_all('a')[0].get('href').strip()
            if url.startswith('https://cs.58.com/') is True:
                tongcheng_url.insert_one({'url': url})

    except requests.exceptions.ConnectionError:
        pass


def get_info(url):
    html = requests.get(url, headers=headers)
    try:
        soup = BeautifulSoup(html.text, 'html.parser')
        titles = soup.select('#basicinfo > div.detail-title > h1')
        prices = soup.select('div > div.infocard__container__item__main > span')
        # areas = soup.select('div:nth-child(3) > div.infocard__container__item__main')
        citys = soup.select('div.infocard__container__item__main > a:nth-child(1)')
        zones = soup.select('div.infocard__container__item__main > a:nth-child(2)')

        pubdates = soup.select('div.detail-title > div.detail-title__info > div:nth-child(1)')
        posts = soup.select('div.shopinfo__intro > dl.shopinfo__intro__last > dt')

        for (title, price, city, zone, pubdate, post) in zip(titles, prices, citys, zones, pubdates, posts):
            loc = city.get_text().strip()
            zone = zone.get_text().strip()

            if len(loc) == 0:
                loc = '无'
            else:
                if len(zone) > 0:
                    loc = loc + '-' + zone
            print(loc)

            price = price.get_text().strip()
            if len(price) == 0:
                price = '无'
            print(price)

            pubdate = pubdate.get_text().strip()
            if len(pubdate) == 0:
                pubdate = '无'
            print(pubdate)

            post = post.get_text().strip()
            if len(post) == 0:
                post = '无'
            print(post)

            info = {
                'title': title.get_text().strip(),
                'price': price,
                'area': loc,
                'date': pubdate,
                'post': post,
                'url': url
            }
            tongcheng_info.insert_one(info)

    except IndexError:
        pass
