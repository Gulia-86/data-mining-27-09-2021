# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose

def clear_price(value):
    try:
        value = ''.join(e for e in value if e.isalnum())
        value = int(value)
    except:
        return value
    return value

class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    photo = scrapy.Field()
    article = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()

