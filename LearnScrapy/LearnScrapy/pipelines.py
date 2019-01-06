# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from .items import XiaoquItem, SellingItem, RentingItem
from scrapy.exceptions import DropItem
from traceback import format_exc

class City58_Pipeline(object):
    def __init__(self, host, port, dbname):
        self.url = 'mongodb://'+host+':'+str(port)
        self.dbname = dbname

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('DB_HOST'), crawler.settings.get('DB_PORT'),
                   crawler.settings.get('MONGO_DB'))

    def open_spider(self,spider):
        self.cli = MongoClient(self.url)
        self.db = self.cli.get_database(self.dbname)

    def process_item(self, item, spider):
        col = self.db.get_collection(item.COL)
        if isinstance(item, XiaoquItem):
            col.ensure_index('name', unique = True)
            try:
                col.update_one({'name': item['name']}, {'$set': item}, upsert=True)
            except:
                spider.logger.error(format_exc())
        else:
            col.insert_one(dict(item))
        raise DropItem()

    def close_spider(self, spider):
        self.cli.close()
