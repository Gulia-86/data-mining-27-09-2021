from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobpars import settings
from jobpars.spiders.hhru import HhruSpider
from jobpars.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)

    process.start()