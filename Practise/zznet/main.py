import sys
sys.path.append("./")
from multiprocessing import Pool
from channel_extract import channel_list
from page_spider import get_links
import time

from page_spider import get_info
from page_spider import tongcheng_url
from page_spider import tongcheng_info


# 阶段一 多线程爬取商品链接
# def get_all_links_from(channel):
#
#     # get_links(channel, 2)
#
#     for num in range(1, 101):
#         get_links(channel, num)
#
#
# if __name__ == '__main__':
#     pool = Pool(processes=4)
#     # get_all_links_from('https://cs.58.com/shouji/')
#
#
# print(channel_list)
# pool.map(get_all_links_from, channel_list)



# 阶段二 根据阶段一爬取的商品链接多线程爬去每个商品的信息
# tongcheng_url数据库存储的链接
db_urls = [item['url'] for item in tongcheng_url.find()]
# 已经爬取的商品中取出链接字段
db_infos = [item['url'] for item in tongcheng_info.find()]
x = set(db_urls)
y = set(db_infos)
# 剩下没有爬取的商品链接
result_urls = x - y
print(len(result_urls))

if __name__ == '__main__':
    # print(db_urls)
    # get_info('https://cs.58.com/shouji/37392868476300x.shtml')
    for url in result_urls:
        print(url)
        get_info(url)
        time.sleep(1)
#     pool = Pool(processes=4)
# pool.map(get_info, result_urls)


