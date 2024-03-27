# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings



class ZaraHmScraperPipeline:
    def process_item(self, item, spider):
        return item
   

class MongoDBPipeline:
    def __init__(self):
        self.settings = get_project_settings()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.settings.get('MONGODB_URI'))
        self.db = self.client[self.settings.get('MONGODB_DB')]
        self.collection = self.db[spider.name] 

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item