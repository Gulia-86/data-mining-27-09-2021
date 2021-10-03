#2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
# больше введённой суммы (необходимо анализировать оба поля зарплаты).

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['db_hh']
hh = db.hh
#без проверки ввода
currency = int(input('Выберите цифру для выбора валюты'
                     '\n1 - рубли'
                     '\n2 - EUR'
                     '\n3 - USD\n'))
#есть ещё другие валюты грн., KZT, KGS, бел. руб... можно и их добаваить

if currency == 1:
    currency = 'руб.'
elif currency == 2:
    currency = 'EUR'
elif currency == 2:
    currency = 'USD'
print(currency, type(currency))
value = int(input('Введите уровень дохода в выбранной валюте: '))

for doc in hh.find({'$and': [{'compensation_currency': currency},
                   {'$or': [{'compensation_min': {'$gt': value}},
                            {'compensation_max': {'$gte': value}}]}]
                    }):
    pprint(doc)
