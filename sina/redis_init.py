#!/usr/bin/env python
# encoding: utf-8
import redis
import sys
import os
import datetime

sys.path.append(os.getcwd())
from sina.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT

r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT)
for key in r.scan_iter("weibo_spider*"):
    r.delete(key)
    print('删除成功')

url_format = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&advancedfilter=1&starttime={}&endtime={}&sort={}&page=1"
# 搜索的关键词，可以修改
keywords = ["战狼", '建党伟业', '靖国神社', '抵制韩货','中国梦','台独','撤侨']
# 搜索的起始日期，可修改 微博的创建日期是2009-08-16 也就是说不要采用这个日期更前面的日期了
date_start = datetime.datetime.strptime("2014-07-30", '%Y-%m-%d')
# 搜索的结束日期，可修改
date_end = datetime.datetime.strptime("2018-11-06", '%Y-%m-%d')
time_spread = datetime.timedelta(days=1)
is_hot = True

'''
while date_start < date_end:
    next_time = date_start + time_spread

    url = url_format.format(keyword, date_start.strftime("%Y%m%d"), next_time.strftime("%Y%m%d"),
                            'hot' if is_hot else 'time')
    
    r.lpush('weibo_spider:start_urls', url)
    date_start = next_time
    print('添加{}成功'.format(url))
'''
for keyword in keywords:
    url = url_format.format(keyword, date_start.strftime("%Y%m%d"), date_end.strftime("%Y%m%d"),
                            'hot' if is_hot else 'time')
    r.lpush('weibo_spider:start_urls', url)
    print('添加{}成功'.format(url))
