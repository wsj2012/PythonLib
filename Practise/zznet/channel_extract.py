import requests
from bs4 import BeautifulSoup
import pymongo
import re

start_url = 'https://cs.58.com/sale.shtml'
url_host = 'https://cs.58.com'

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}


channel_list = []


def get_channel_urls(url):
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    infos = soup.select('ul > li > ul > li > b > a')

    for (info) in zip(infos):
        # print(url_host + info[0].get('href'))
        channel_list.append(url_host + info[0].get('href'))


get_channel_urls(start_url)


# if __name__ == '__main__':
#
#     get_channel_urls(start_url)


