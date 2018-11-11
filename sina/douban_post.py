import pymongo
from sina.douban_settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME_POST, DB_NAME
from pymongo.errors import DuplicateKeyError
import time
import datetime

years = [2018,2017,2016,2015,2014,2013,2012,2011,2010]
types = ['搞笑','文艺','科幻','惊悚', '爱国','红色','共产党']
class Tweet(object):
    def __init__(self):
        self.item = dict()
        pass

    def insertTweetsItem(self, TweetsItem):
        self.item = TweetsItem
        self.item['comments'] = []
        self.item['star_count']=[dict()]

    def insertInformationItems(self, InformationItems):
        for item in InformationItems:
            self.insertInformationItem(item)
            break

    def insertInformationItem(self, InformationItem):
        if InformationItem is not None:
            self.item['information'] = InformationItem

    def insertComments(self, CommentItems):
        number = 0
        for item in CommentItems:
            self.insertComment(item,self.item['star_count'][0])
            number += 1
        return number

    def insertComment(self, CommentItem,star):
        if CommentItem is not None and self.filter(CommentItem):
            if not self.item.get('comments', False):
                self.item['comments'] = []
            self.item['comments'].append(CommentItem)
            if CommentItem.get('star', False):
                try:
                    star[CommentItem['star']] = star.get(CommentItem['star'], 0) + int(CommentItem['star'])
                except Exception as e:
                    self.logger.error(e)

    def filter(self, Item):

        return True


class PostProcessing(object):
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.db = client[DB_NAME_POST]
        self.search_db = client[DB_NAME]
        self.comment_total = dict()
        self.movie_total = dict()
        self.total=0

    def begin(self):
        for tweet in self.search_db.Movies.find():
            self.log('movie:\n{}'.format(tweet))
            item = Tweet()
            self.total += 1
            item.insertTweetsItem(tweet)
            item.insertInformationItems(self.search_db.Infos.find({'id_movie': tweet['id']}))
            number = item.insertComments(self.search_db.Comment.find({'id_movie': tweet['id']}))

            index = 0
            try:
                index = types.index(tweet['style'])
            except Exception as e:
                self.logger.error(e)
            self.insert_item(self.db['movie{}{}'.format(index, tweet['year'])], item.item)

            self.log('{} comments number is {}'.format(item.item['title'], number))

            if not self.comment_total.get('movie{}{}'.format(index, tweet['year']), False):
                self.comment_total['movie{}{}'.format(index, tweet['year'])] = number
            self.comment_total['movie{}{}'.format(index, tweet['year'])] += number

            if not self.movie_total.get('movie{}{}'.format(index, tweet['year']), False):
                self.movie_total['movie{}{}'.format(index, tweet['year'])] = 1
            self.movie_total['movie{}{}'.format(index, tweet['year'])] += 1

        self.end()

    def end(self):
        self.log('------movie_total:')
        for key in self.movie_total:
            self.log('{}:{}'.format(key, self.movie_total[key]))
        self.log('------comment_total:')
        for key in self.comment_total:
            self.log('{}:{}'.format(key, self.comment_total[key]))

        self.log('total movie:{}'.format(self.total))

    def log(self, message):
        with open('log.txt', 'a', encoding='utf-8') as file:
            print(message, file=file)

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(item)
        except DuplicateKeyError:
            print('-------------DuplicateKeyError-------------')
            """
            说明有重复数据
            """
            pass


if __name__ == '__main__':
    postProcessing = PostProcessing()
    postProcessing.begin()
