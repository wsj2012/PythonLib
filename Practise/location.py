import requests
import json
import pprint

address = input('请输入地点：')
params = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
url =  'http://restapi.amap.com/v3/geocode/geo'
res = requests.get(url, params)
json_data = json.loads(res.text)
geo = json_data['geocodes'][0]['location']
pprint.pprint(geo)
