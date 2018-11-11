# -*- coding: utf-8 -*-
import json
import re
from lxml import etree
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from scrapy_redis.spiders import RedisSpider
from sina.items import TweetsItem, InformationItem, CommentItem
from sina.spiders.utils import time_fix
import time
import urllib


class DouBanSpider(RedisSpider):
    name = "douban_spider"
    base_url = "https://www.douban.com/"
    redis_key = "douban_spider:start_urls"
    limit_movie_page = 5000
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        "DOWNLOAD_DELAY": 1,
    }

    def parse(self, response):
        """
        解析本页的数据
        """

        try:
            movieItems = json.loads(response.body, encoding='GBK')['data']
            print(movieItems)
            print(len(movieItems))
            if len(movieItems) == 0:
                url = urllib.parse.unquote(response.url)
                style = str(url.split('&')[-3].split(',')[-1])
                year = re.findall(r'year_range=(\d*),', response.url)[0]
                for item in response.meta.get('movies', []):
                    item['_diff'] = 'movie'
                    item['year'] = year
                    item['style'] = style
                    yield item
                    yield Request(item['url'], callback=self.parse_further, meta={'movie': item}, priority=1)
                return

            # 获取下一页
            page = re.findall(r'start=\d*', response.url)[0]
            page_number = page.split('=')[-1]
            page_number = int(page_number) + 20

            page_url = response.url.replace(page, 'start={}'.format(page_number))

            if response.meta.get('movies', False):
                response.meta['movies'] += (movieItems)
                print('now is ', len(response.meta['movies']))
                yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)
            else:
                yield Request(page_url, self.parse, dont_filter=True, meta={'movies': movieItems})

        except Exception as e:
            self.logger.error(e)

    def parse_further(self, response):
        # parse

        # 解析相关数据
        try:
            tree_node = etree.HTML(response.body.decode("UTF-8"))
            tweet_nodes = tree_node.xpath('//div[@id="interest_sectl"]/div[@class="rating_wrap clearbox"]')
            item = dict()
            item['id_movie'] = response.meta['movie']['id']
            item['_diff'] = 'info'
            for node in tweet_nodes:
                for i in node.xpath('.//a[@class="rating_people"]/span/text()'):
                    if len(i) == 0:
                        break
                    item['votes'] = i
                    break
                for i in node.xpath('.//div[@class="rating_right "]/div[1]/@class'):
                    temp = re.findall(r'll bigstar bigstar(\d*)', i)
                    if len(temp) == 0:
                        break
                    item['star_aver'] = temp[0]
                    print('star_aver', item['star_aver'])
                    break
                number = 5
                for i in node.xpath(
                        './/div[@class="ratings-on-weight"]/div[@class="item"]/span[@class="rating_per"]/text()'):
                    item['star{}'.format(number)] = i
                    number -= 1
                    if number == 0:
                        break
                break

            tweet_nodes = tree_node.xpath('.//div[@id="info"]')
            item['release_date'] = []
            for node in tweet_nodes:
                for i in node.xpath(
                        './/span[text()="上映日期:"]/following-sibling::span[@property="v:initialReleaseDate"]/text()'):
                    print(i)
                    item['release_date'].append(i)

            reviews_url = response.url + '/reviews'
            yield Request(reviews_url, self.parse_comments, dont_filter=True, meta={'item': item})
            yield item
        except Exception as e:
            print(e)
            self.logger.error(e)

    def parse_comments(self, response):
        try:
            tree_node = etree.HTML(response.body.decode("UTF-8"))
            # 获取下一页
            for url in tree_node.xpath(
                    './/div[@class="paginator"]/span[@class="thispage"]/following-sibling::a/@href'):
                if response.url.find('?') != -1:
                    url = response.url[0:response.url.find('?')] + url
                else:
                    url = response.url + url
                print('nextpage', url)
                yield Request(url, self.parse_comments, dont_filter=True, meta=response.meta)
                break

            # 解析
            tweet_nodes = tree_node.xpath('.//div[@class="main review-item"]')
            for node in tweet_nodes:
                item = dict()
                item['_diff'] = 'comment'
                item['id_movie'] = response.meta['item']['id_movie']
                print('begin')
                for i in node.xpath('.//span[contains(@class,"main-title-rating")]/@class'):
                    list_star = re.findall(r'allstar(\d*) main-title-rating', i)
                    if len(list_star) != 0:
                        item['star'] = list_star[0]
                        print('star', item['star'])
                    break
                for i in node.xpath(
                        './/span[contains(@class,"main-title-rating")]/following-sibling::span[@class="main-meta"]/@content'):
                    item['time'] = i
                    print('time', item['time'])
                    break
                for i in node.xpath('.//div[@class="short-content"]/text()'):
                    item['content'] = i
                    print('content', item['content'])
                    break
                for i in node.xpath('.//div[@class="short"]/text()'):
                    item['content'] = i
                    print('content', item['content'])
                    break
                for i in node.xpath('.//div[contains(@class,"main-bd")]/h2/a/text()'):
                    item['title'] = i
                    print('title', item['title'])
                    break
                yield item
                print('end')
        except Exception as e:
            print(e)
            self.logger.error(e)


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl('douban_spider')
    process.start()
