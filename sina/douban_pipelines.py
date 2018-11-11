# -*- coding: utf-8 -*-
import pymongo
from pymongo.errors import DuplicateKeyError
from sina.items import RelationshipsItem, TweetsItem, InformationItem, CommentItem
from sina.douban_settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME


class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = client[DB_NAME]
        self.Movies = db["Movies"]
        self.Infos = db["Infos"]
        self.Comment = db["Comment"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if item.get('_diff', None) == 'movie':
            self.insert_item(self.Movies, item)
        elif item.get('_diff', None) == 'info':
            self.insert_item(self.Infos, item)
        elif item.get('_diff', None) == 'comment':
            self.insert_item(self.Comment, item)
        print(item.get('_diff', None), item)
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(item)
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            print('-------------DuplicateKeyError-------------')
            pass
