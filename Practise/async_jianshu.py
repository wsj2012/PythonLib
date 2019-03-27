import requests
from lxml import etree
import pymongo

client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
timeline = mydb['timeline']

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}


def get_time_info(url, page):
    user_id = url.split('/')[4]
    page = page + 1
    # if url.find('page=') == -1:
    #     print(url)
    #     page = page + 1
    #     print('hello' + str(page))
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    # print(html.text)
    infos = selector.xpath('//ul[@class="note-list"]/li')
    print('heill')
    for info in infos:
        dd = info.xpath('div/div/div/span/@data-datetime')[0]
        type = info.xpath('div/div/div/span/@data-type')[0]
        timeline.insert_one(({'date': dd, 'type': type}))

    id_infos = selector.xpath('//ul[@class="note-list"]/li/@id')
    if len(id_infos) > 0:
        feed_id = id_infos[-1]
        max_id = feed_id.split('-')[1]
        max_id = str(int(max_id) - 1)
        print(max_id)
        next_url = 'https://www.jianshu.com/users/%s/timeline?max_id=%s&page=%s' % (user_id, max_id, page)
        print(next_url)
        get_time_info(next_url, page)


if __name__ == '__main__':
    get_time_info('https://www.jianshu.com/users/9be53b53e632/timeline', 1)

