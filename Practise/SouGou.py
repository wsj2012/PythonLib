# -*- coding:utf-8 -*-

import Logger
import requests
from bs4 import BeautifulSoup
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

def get_info(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    ranks = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_num')
    singer_songs = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > a')
    times = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_tips_r > span')
    for rank, singer_song, time in zip(ranks, singer_songs, times):
        data = {
            'rank': rank.get_text().strip(),
            'singer': singer_song.get_text().split('-')[0],
            'song': singer_song.get_text().split('-')[1],
            'time': time.get_text().strip()
        }
        Logger.log(data)


if __name__ == '__main__':
    urls = ['https://www.kugou.com/yy/rank/home/{}-8888.html?from=rank'.format(number) for number in range(1, 6)]
    for url in urls:
        get_info(url)
        time.sleep(3)