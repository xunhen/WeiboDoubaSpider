#!/usr/bin/env python
# encoding: utf-8
import redis
import sys
import os
import datetime

sys.path.append(os.getcwd())
from sina.douban_settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT

r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT)
for key in r.scan_iter("douban_spider*"):
    r.delete(key)
    print('删除成功')

url_format = "https://movie.douban.com/j/new_search_subjects?sort={}&range=0,10&tags=中国大陆,电影,{}&start=0&year_range={},{}"

years = [2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]
types = ['搞笑', '文艺', '科幻', '惊悚', '爱国', '红色', '共产党']


def convert(*param):
    s = ''
    for i in param:
        s += str(i) + ','
    s = s[0:-1]
    return s


year = [6, 7, 8]
type = [0, 1, 2, 3, 4, 5, 6]
for year_ in year:
    for type_ in type:
        url = url_format.format('S', types[type_], years[year_], years[year_])
        r.lpush('douban_spider:start_urls', url)
        print('添加{}成功'.format(url))

'''
for year in years:
    for type_ in types:
        url = url_format.format('S', type_, year, year)
        r.lpush('douban_spider:start_urls', url)
        print('添加{}成功'.format(url))
'''
