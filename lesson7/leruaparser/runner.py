from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leruaparser.spiders.leroy import LeroySpider
from leruaparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroySpider, query='Теплоноситель')
    process.start()

