import requests
from lxml import etree
import re
from bs4 import BeautifulSoup
import pymongo
import time

client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
musictop = mydb['musictop']
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}


def get_url_music(url):
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    music_hrefs = soup.find_all('tr', class_="item")
    for (link) in zip(music_hrefs):
        hrefs = link[0].find_all('a')[0].get('href')
        get_music_info(hrefs)

def get_music_info(link):
    html = requests.get(link, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    names = soup.select('#wrapper > h1 > span')
    authors = soup.select('#info > span > span > a')
    styles = re.findall('<span class="pl">流派:</span>&nbsp;(.*?)<br />', html.text, re.S)
    times = re.findall('<span class="pl">发行时间:</span>&nbsp;(.*?)<br />', html.text, re.S)
    publishers = re.findall('<span class="pl">出版者:</span>&nbsp;(.*?)<br />', html.text, re.S)
    scores = soup.select('#interest_sectl > div > div.rating_self.clearfix > strong')

    for (name, author, style, time, publisher, score) in zip(names, authors, styles, times, publishers, scores):
        if len(style) == 0:
            style = '未知'
        else:
            style = style.strip()
        print(name.get_text(), author.get_text(), style, time.strip(), publisher.strip(), score.get_text())

        info = {
            'name': name.get_text(),
            'author': author.get_text(),
            'style': style,
            'time': time.strip(),
            'publisher': publisher.strip(),
            'score': score.get_text()
        }
        musictop.insert_one(info)


if __name__ == '__main__':
    urls = ['https://music.douban.com/top250?start={}'.format(str(i))
            for i in range(0, 250, 25)]
    for url in urls:
        get_url_music(url)
        time.sleep(1)
