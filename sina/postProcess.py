import pymongo
from sina.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME_POST, DB_NAME
from pymongo.errors import DuplicateKeyError
import time
import datetime


class Tweet(object):
    def __init__(self):
        self.item = dict()
        pass

    def insertTweetsItem(self, TweetsItem):
        self.item = TweetsItem
        self.item['comments'] = []
        self.item['comments_year98-01'] = []
        self.item['comments_year95-98'] = []
        self.item['comments_year92-95'] = []
        self.item['information'] = []

    def insertInformationItems(self, InformationItems):
        for item in InformationItems:
            self.insertInformationItem(item)
            break

    def insertInformationItem(self, InformationItem):
        if InformationItem is not None:
            self.item['information'].append(InformationItem)

    def insertComments(self, CommentItems):
        number = 0
        for item in CommentItems:
            self.insertComment(item)
            number += 1
        return number

    def insertComment(self, CommentItem):
        if CommentItem is not None and self.filter(CommentItem):
            self.item['comments'].append(CommentItem)

    def insertComentAndInfo(self, CommentItem, InformationItem):
        which = -1

        if CommentItem is not None:
            for info in InformationItem:
                CommentItem['information'] = info
                print(info)
                if info is not None and self.isInyears(info.get('birthday', 0), 1998, 2001):
                    self.item['comments_year98-01'].append(CommentItem)
                    which = 3
                elif info is not None and self.isInyears(info.get('birthday', 0), 1995, 1998):
                    self.item['comments_year95-98'].append(CommentItem)
                    which = 2
                if info is not None and self.isInyears(info.get('birthday', 0), 1992, 1995):
                    self.item['comments_year92-95'].append(CommentItem)
                    which = 1
                break

            self.item['comments'].append(CommentItem)
        return which

    def isInyears(self, birth, startyear, endyear):
        try:
            birthyear = int(birth.split('-')[0])
            startyear = int(startyear)
            endyear = int(endyear)
            if (birthyear >= startyear and birthyear < endyear):
                return True
            return False
        except:

            return False

    def filter(self, Item):

        return True


class PostProcessing(object):
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.db = client[DB_NAME_POST]
        self.search_db = client[DB_NAME]
        self.tweets = self.db["Tweets"]

        self.infos_total = 0
        self.tweets_total = 0
        self.comments_total = 0
        self.comments98_01_total = 0
        self.comments95_98_total = 0
        self.comments92_95_total = 0

    def begin(self):
        for tweet in self.search_db.Tweets.find():
            self.log('tweet:\n{}'.format(tweet))
            item = Tweet()
            self.tweets_total += 1
            item.insertTweetsItem(tweet)
            item.insertInformationItems(self.search_db.Information.find({'_id': tweet['user_id']}))
            number = item.insertComments(self.search_db.Comments.find({'weibo_url': tweet['weibo_url']}))
            for comment in self.search_db.Comments.find({'weibo_url': tweet['weibo_url']}):
                which = item.insertComentAndInfo(comment,
                                                 self.search_db.Information.find({'_id': comment['comment_user_id']}))
                if which == 1:
                    self.comments92_95_total += 1
                elif which == 2:
                    self.comments95_98_total += 1
                elif which == 3:
                    self.comments98_01_total += 1

            self.insert_item(self.tweets, item.item)
            self.log('information:\n{}'.format(item.item['information']))
            self.log('comments size:{}'.format(number))
            self.comments_total += number

        self.end()

    def end(self):
        self.log('comments_total:{}'.format(self.comments_total))
        self.log('comments92_95_total:{}'.format(self.comments92_95_total))
        self.log('comments95_98_total:{}'.format(self.comments95_98_total))
        self.log('comments98_01_total:{}'.format(self.comments98_01_total))
        self.log('tweets_total:{}'.format(self.tweets_total))

    def test(self):
        for tweet in self.search_db.Tweets.find():

            print(tweet)
            for i in self.search_db.Information.find({'_id': tweet['user_id']}):
                print(i)
            for i in self.search_db.Comments.find({'weibo_url': tweet['weibo_url']}):
                print(i)

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
