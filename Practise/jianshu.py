import requests
from bs4 import BeautifulSoup
import re
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
jianshu_shouye = mydb['jianshu_shouye']

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}

def get_jianshu_info(url):
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    authors = soup.find_all('a', class_='nickname')
    titles = soup.find_all('div', class_='content')
    contents = soup.find_all('p', class_='abstract')
    comments = re.findall('<i class="iconfont ic-list-comments">.*?</i>(.*?)</a>', html.text, re.S)
    likes = re.findall('<i class="iconfont ic-list-like">.*?</i>(.*?)</span>', html.text, re.S)
    rewards = re.findall('<i class="iconfont ic-list-money">.*?</i>(.*?)</span>', html.text, re.S)

    for (author, title, content, comment, like, reward) in zip(authors, titles, contents, comments, likes, rewards):
        # print(author.get_text(), title.find_all('a')[0].get_text())
        # print(comment.strip())
        # print(like.strip())
        reward = reward.strip()
        if len(reward) == 0:
            reward = "无"
            print(reward)
        else:
            print(reward)
        # print(content.get_text())
        # print(title[0].find_all('a')[0].get_text())
        # print(title[0])

        data = {
            'title': title.find_all('a')[0].get_text(),
            'author': author.get_text(),
            'content': content.get_text(),
            'comment': comment.strip(),
            'like': like.strip(),
            'reward': reward
        }
        jianshu_shouye.insert_one(data)



if __name__ == '__main__':
    urls = ['https://www.jianshu.com/c/bDHhpK?order_by=commented_at&page={}'.format(str(i))
            for i in range(1, 500)]
    # get_jianshu_info('https://www.jianshu.com/c/bDHhpK?order_by=commented_at&page=0')
    # for url in urls:
    #     get_jianshu_info(url)
    pool = Pool(processes=4)
    pool.map(get_jianshu_info, urls)

