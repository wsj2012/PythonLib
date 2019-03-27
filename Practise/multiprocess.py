import requests
import re
import time
from bs4 import BeautifulSoup
from multiprocessing import Pool

headers = requests.utils.default_headers()
headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

def re_scraper(url):
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    ids = re.findall('<h2>(.*?)</h2>', html.text, re.S)
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>', html.text, re.S)
    laughs = re.findall('<span class="stats-vote"><i class="number">(.*?)</i>', html.text, re.S)
    comments = soup.find_all('span', class_='stats-comments')
    for (name, content, laugh, comment) in zip(ids, contents, laughs, comments):
        info = {
            'id': str(name),
            'content': str(content),
            'laugh': str(laugh),
            'comment': comment.find_all('i')[0].get_text()
        }
        return info

        # print(str(name))
        # print(str(content))
        # print(str(laugh))
        # print(comment.find_all('i')[0].get_text())


if __name__ == '__main__':
    urls = ['https://www.qiushibaike.com/text/page/{}/'.format(str(i))
            for i in range(1, 10)]
    # 单线程
    start_1 = time.time()
    for url in urls:
        re_scraper(url)
    end_1 = time.time()
    print('串行爬虫', end_1-start_1)

    # 多线程 2个线程
    start_2 = time.time()
    pool = Pool(processes=2)
    pool.map(re_scraper, urls)
    end_2 = time.time()
    print('两个线程', end_2-start_2)

    # 多线程 4个线程
    start_3 = time.time()
    pool1 = Pool(processes=4)
    pool1.map(re_scraper, urls)
    end_3 = time.time()
    print('4个线程', end_3-start_3)