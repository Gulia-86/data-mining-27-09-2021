import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leruaparser.items import LeruaparserItem

class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://tyumen.leroymerlin.ru/search/?q={query}']

    def parse(self, response):
        links = response.xpath("//a[@data-qa='product-name']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('photo', '//img[@alt="product image"]/@src')
        loader.add_xpath('article', '//span[@slot="article"]/@content')
        yield loader.load_item()
