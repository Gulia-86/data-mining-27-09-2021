# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparsPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy1110


    def process_item(self, item, spider):
        item['currency'] = self.process_salary_cur(item['salary'])
        item['salary_min'] = self.process_salary_min(item['salary'])
        item['salary_max'] = self.process_salary_max(item['salary'])

        del item['salary']
        if spider.name == 'hhru':
            pass
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_cur(self, salary):
        currency = None
        #следующий цикл пришлось сделать, так как на sjru попались числа с валютой вместе, например: 90000руб.
        for i in range(0, len(salary)):
            if re.findall(r"руб.", salary[i]):
                currency = 'руб.'
                salary[i] = salary[i].replace('руб.','')
            if re.findall(r"EUR",salary[i]):
                currency = 'EUR'
                salary[i] = salary[i].replace('EUR','')
            if re.findall(r"USD",salary[i]):
                currency = 'USD'
                salary[i] = salary[i].replace('USD','')
            #здесь же удалим лишние символы
            salary[i] = ''.join(e for e in salary[i] if e.isalnum())
            salary[i] = salary[i].replace("\xa0", "")
            try:
                salary[i] = int(salary[i])
            except:
                pass

        return currency

    def process_salary_min(self, salary):
        salary_min = None
        spam = []
        for i in salary:
            if type(i) is int:
                spam.append(i)
        if 'от' in salary:
            salary_min = min(spam)
        if len(spam) > 1:
            salary_min = min(spam)

        return salary_min

    def process_salary_max(self, salary):
        salary_max = None
        spam = []
        for i in salary:
            if type(i) is int:
                spam.append(i)
        if 'до' in salary:
            salary_max = max(spam)
        if len(spam) > 1:
            salary_max = max(spam)
        return salary_max

