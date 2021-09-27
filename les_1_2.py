#2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests, json

headers = {
    'X-Yandex-API-Key': token
}

lat = 57
lon = 65
lang = "ru_RU"
url = "https://api.weather.yandex.ru/v2/forecast?"

r = requests.get(f'{url}{lat}&{lon}&{lang}', headers = headers)
with open('data2.json', 'w') as f:
    json.dump(r.text, f)

