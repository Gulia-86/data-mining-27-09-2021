# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import scrapy

class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['instagram']


    def process_item(self, item, spider):
        collection = self.mongo_base['instaparse']
        if item['relation'] == 'follower':
            try:
                collection.update_one({'follower_username': item['follower_username']}, {'$set': item}, upsert=True)

            except Exception as exc:
                print('Что-то пошло не так/n', exc)

        if item['relation'] == 'following':
            try:
                collection.update_one({'following_username': item['following_username']}, {'$set': item}, upsert=True)

            except Exception as exc:
                print('Что-то пошло не так/n', exc)

        return item

class InstaparserPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

