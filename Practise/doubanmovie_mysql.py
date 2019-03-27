import requests
from bs4 import BeautifulSoup
import re
import pymysql
import pymongo
import time

conn = pymysql.connect(host='localhost', user='root', passwd='wang.li.708', db='testmysql', port=3306, charset='utf8')
cursor = conn.cursor()

client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
movietop = mydb['movietop']

headers = requests.utils.default_headers()
headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'


def get_movie_url(url):
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')

    movie_hrefs = soup.find_all('div', class_='hd')
    for (movie_href) in zip(movie_hrefs):
        href = movie_href[0].find_all('a')[0].get('href')
        get_movie_info(href)


def get_movie_info(link):
    html = requests.get(link, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    try:
        names = soup.select('#content > h1 > span')
        directors = soup.select('#info > span > span.attrs > a')
        actors = soup.select('#info > span.actor > span.attrs')
        styles = re.findall('<span property="v:genre">(.*?)</span', html.text, re.S)
        countrys = re.findall('<span class="pl">制片国家/地区:</span>(.*?)<br/>', html.text, re.S)
        release_times = re.findall('<span property="v:initialReleaseDate" content="(.*?)">', html.text, re.S)
        times = re.findall('<span property="v:runtime" content="(.*?)">', html.text, re.S)
        scores = re.findall('<strong class="ll rating_num" property="v:average">(.*?)</strong>', html.text, re.S)

        if len(styles) > 0:
            style = styles[0]
        if len(styles) > 1:
            for i in range(len(styles)):
                if i > 0:
                    style = style + "/" + styles[i]

        # print(style)

        if len(release_times) > 0:
            release_date = release_times[0]
        if len(release_times) > 1:
            for i in range(len(release_times)):
                if i > 0:
                    release_date = release_date + "/" + release_times[i]
        time = times[0] + "分钟"
        score = scores[0]

        for (name, director, actor, county) in zip(names, directors, actors, countrys):
            print(name.get_text())
            # name.get_text(), director.get_text(),
            # print(name.get_text(), director.get_text())
            # print(actor.get_text())

            info = {
                'name': name.get_text(),
                'director': director.get_text(),
                'actor': actor.get_text(),
                'style': style,
                'country': county.strip(),
                'release_time': str(release_date),
                'time': str(time),
                'score': str(score)
            }

            movietop.insert_one(info)

            cursor.execute(
                "insert into doubanmovie (name, director, actor, style, country, release_time, time, score) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                (str(name.get_text()), str(director.get_text()), str(actor.get_text()), str(style), str(county.strip()),
                 str(release_date), str(time), str(score)))

    except IndexError:
        pass

if __name__ == '__main__':
    urls = ['https://movie.douban.com/top250?start={}'.format(str(i))
            for i in range(0, 25, 25)]
    for url in urls:
        get_movie_url(url)
        time.sleep(2)
    conn.commit()
