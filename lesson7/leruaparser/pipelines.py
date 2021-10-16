# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class LeruaparserPipeline:
    def process_item(self, item, spider):
        print()
        return item

class LeruaPhotosPipeline(ImagesPipeline):
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

    def file_path(self, request, response=None, info=None, *, item=None):
        image_name = request.url.split('/')[-1]
        #folder = item['article']
        #не самый удачный вариант по артикулу, в ссылке он и так есть
        #поменяла на название категории
        filename = u'{0}/{1}'.format('теплоноситель', image_name)
        return filename
