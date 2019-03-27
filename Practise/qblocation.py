import requests
from bs4 import BeautifulSoup
import csv
import json
import pprint

fp = open('/Users/wangshujun566/Desktop/qbl.csv', 'w+', newline="")
csvwriter = csv.writer(fp)
csvwriter.writerow(('address', 'long', 'lati'))

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

host = 'https://www.qiushibaike.com'
user_profiles = []

def get_user_id(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    id_info = soup.select('div > a')
    for (id) in zip(id_info):
        # print(id[0].get('href'))
        if len(id[0].get('href').split('/users/')) > 1:
            user_profiles.append(host + id[0].get('href') + '/')

    for adurl in user_profiles:
        get_address(adurl)

def get_address(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    address = soup.select('div > ul > li:nth-child(4)')
    for add in zip(address):
        print(add[0].get_text())
        if len(add[0].get_text().split('故乡:')) > 1:
            get_geo(add[0].get_text().split('故乡:')[1])


def get_geo(address):
    params = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
    url = 'http://restapi.amap.com/v3/geocode/geo'
    res = requests.get(url, params)
    json_data = json.loads(res.text)
    if 'geocodes' in res.text and 'location' in res.text:
        print(json_data['geocodes'])
        geo = json_data['geocodes'][0]['location']
        pprint.pprint(geo)
        csvwriter.writerow((address, geo.split(',')[0], geo.split(',')[1]))

if __name__ == '__main__':
    urls = ['https://www.qiushibaike.com/8hr/page/{}/'.format(str(number)) for number in range(1, 3)]
    for url in urls:
        get_user_id(url)