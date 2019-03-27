import requests
from bs4 import BeautifulSoup
import json

path = '/Users/wangshujun566/Desktop/love/'

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


def get_image_info(url):
    wb_data = requests.get(url, headers=headers)
    print(wb_data.text)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    imgs = soup.select('div.photos > div > div > article > a > img')

    lists = []
    for img in imgs:
        photo = img.get('src')
        print(photo)
        lists.append(photo)
    for item in lists:
        data = requests.get(item, headers=headers)
        fp = open(path + item.split('?')[0][-10:], 'wb')
        fp.write(data.content)
        fp.close()


if __name__ == '__main__':
    url_path = 'https://www.pexels.com/search/'
    word = input('请输入你要检索的关键词：')
    print(word)
    urls = ['https://www.pexels.com/search/{}/?page={}'.format(word, str(i))
            for i in range(1, 10)]
    for url in urls:
        get_image_info(url)
