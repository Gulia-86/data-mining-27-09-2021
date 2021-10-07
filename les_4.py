#Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
#Для парсинга использовать XPath. Структура данных должна содержать:
#название источника;
#наименование новости;
#ссылку на новость;
#дата публикации.
#Сложить собранные новости в БД

from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['db_news']
base = db.news

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

response = requests.get("https://yandex.ru/news", headers=header)
dom = html.fromstring(response.text)

items = dom.xpath("//article[contains(@class, 'mg-card')]")

all_news = []
for item in items:
    news = {}
    #название источника
    source = item.xpath(".//a[@class = 'mg-card__source-link']/text()")
    #наименование новости
    name = item.xpath(".//h2[@class = 'mg-card__title']/text()")
    name = str(name).replace("\\xa0", " ") #удаляем $nbsp
    #ссылку на новость
    link = item.xpath(".//a[@class = 'mg-card__link']/@href")
    #дата публикации, в этом случае время
    time = item.xpath(".//span[@class = 'mg-card-source__time']/text()")

    news['source'] = source
    news['name'] = name
    news['link'] = link
    news['time'] = time
    all_news.append(news)
    try:
        base.update_one({'link': news['link']}, {'$set': news}, upsert=True)
    except Exception as exc:
        print('Что-то пошло не так/n', exc)
        continue

pprint(all_news)
