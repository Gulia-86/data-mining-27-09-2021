#1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию.
# Добавить в решение со сбором вакансий(продуктов) функцию, которая будет добавлять только новые вакансии/продукты в вашу базу.

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
import requests
import re
from bs4 import BeautifulSoup as bs
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['db_hh']
hh = db.hh

url = 'https://hh.ru/'
params = {'page': 1}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

pos = input('Введите искомую должность: ')
position_data = {}
while True:
    response = requests.get(url + 'search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=' + pos, headers=headers, params=params)
    soup = bs(response.text, 'html.parser')

    position_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    if not position_list or not response.ok:
        break
    positions = []

    for position in position_list:
        position_data = {}
        position_info = position.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})
        position_name = position_info.text
        position_link = position_info['href']
        position_compensation = position.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
        try:
            position_compensation = position_compensation.text
        except:
            position_compensation = None
            position_compensation_min = None
            position_compensation_max = None
            position_compensation_cur = None

        if position_compensation:
            if position_compensation.find("руб."):
                position_compensation_cur = 'руб.'
                position_compensation = position_compensation.replace('руб.','')
            elif position_compensation.find("EUR"):
                position_compensation_cur = 'EUR'
                position_compensation = position_compensation.replace('EUR','')
            elif position_compensation.find("USD."):
                position_compensation_cur = 'USD'
                position_compensation = position_compensation.replace('USD','')

        if position_compensation:
            if position_compensation.find("–") != -1:
                position_compensation_min = position_compensation.partition("–")[0]
                list = re.findall(r"\d+",position_compensation_min)
                position_compensation_min = int("".join([str(l) for l in list]))
                position_compensation_max = position_compensation.partition("–")[2]
                list = re.findall(r"\d+",position_compensation_max)
                position_compensation_max = int("".join([str(l) for l in list]))

            elif position_compensation.find("от") != -1:
                list = re.findall(r"\d+",position_compensation)
                position_compensation_min = int("".join([str(l) for l in list]))
                position_compensation_max = None

            elif position_compensation.find("до") != -1:
                list = re.findall(r"\d+",position_compensation)
                position_compensation_max = int("".join([str(l) for l in list]))
                position_compensation_min = None


        position_data['name'] = position_name
        position_data['link'] = position_link
        position_data['compensation_min'] = position_compensation_min
        position_data['compensation_max'] = position_compensation_max
        position_data['compensation_currency'] = position_compensation_cur

#проверка записи в БД по ссылке
        # если нет, добавляем

        if hh.find_one({'link': position_link}) == None:
            pprint(position_data)
            try:
                hh.insert_one(position_data)
            except dke:
                print('Document already exist')
        else:
            print('Запись существует')

    params['page'] += 1



