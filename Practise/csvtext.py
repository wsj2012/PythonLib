# -*- coding:utf-8 -*-

import csv

fp = open('/Users/wangshujun566/Desktop/test.csv', 'w+', newline="")
csvwriter = csv.writer(fp)
csvwriter.writerow(('id', 'name'))
csvwriter.writerow(('1', '小明'))
csvwriter.writerow(('2', '张三'))
csvwriter.writerow(('3', '李四'))
