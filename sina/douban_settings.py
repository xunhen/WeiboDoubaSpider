# -*- coding: utf-8 -*-

BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'

ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Cookie': 'bid=lVK7TCDsClw; douban-fav-remind=1; ll="118172"; __utmc=30149280; __utmc=223695111; __yadk_uid=DdlVNsqwA8SJkjbPBwIjM92ISgoQYjI7; _vwo_uuid_v2=D95EB225E82DA05888CBF1ABAD30786C4|fa76dc60191657dc8b9e2d98ba4623d8; ps=y; ct=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.18710; ap_v=0,6.0; __utma=30149280.1363516572.1532181823.1541811454.1541820710.12; __utmz=30149280.1541820710.12.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; douban-profile-remind=1; __utmz=223695111.1541820719.7.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1541823209%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1960076136.1541753585.1541820719.1541823209.8; __utmb=223695111.0.10.1541823209; __utmt=1; as="https://sec.douban.com/b?r=https%3A%2F%2Fbook.douban.com%2F"; dbcl2="187105828:/0XPOJYTWfU"; ck=ICjY; __utmt_douban=1; __utmb=30149280.26.10.1541820710; gr_user_id=42b4f849-c41a-43ab-ac0f-65b5ea0edd94; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=918c7066-e642-4f9f-aef9-5149ddc0131a; gr_cs1_918c7066-e642-4f9f-aef9-5149ddc0131a=user_id%3A1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_918c7066-e642-4f9f-aef9-5149ddc0131a=true; _pk_id.100001.4cf6=377a921cfd355eb2.1541753584.8.1541826229.1541821320.'
}

# CONCURRENT_REQUESTS 和 DOWNLOAD_DELAY 根据账号池大小调整 目前的参数是账号池大小为200

CONCURRENT_REQUESTS = 1

DOWNLOAD_DELAY = 1

#test
CONCURRENT_REQUESTS = 1

DOWNLOAD_DELAY = 1


DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'sina.middlewares.CookieMiddleware': 300,
    'sina.middlewares.RedirectMiddleware': 200,
}

ITEM_PIPELINES = {
    'sina.douban_pipelines.MongoDBPipeline': 300,
}

# MongoDb 配置

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'Douban4'
DB_NAME_POST = 'Douban4_wjc'

# Redis 配置
LOCAL_REDIS_HOST = '127.0.0.1'
LOCAL_REDIS_PORT = 6379

# Ensure use this Scheduler
SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"

# Redis URL
REDIS_URL = 'redis://{}:{}'.format(LOCAL_REDIS_HOST, LOCAL_REDIS_PORT)

# Number of Hash Functions to use, defaults to 6
BLOOMFILTER_HASH_NUMBER = 6

# Redis Memory Bit of Bloomfilter Usage, 30 means 2^30 = 128MB, defaults to 30
BLOOMFILTER_BIT = 31

# Persist
SCHEDULER_PERSIST = True
