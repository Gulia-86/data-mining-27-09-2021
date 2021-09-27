#1. Посмотреть документацию к API GitHub, разобраться как вывести список
# репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

url = 'https://api.github.com'
user = 'Gulia-86'

r = requests.get(f'{url}/users/{user}/repos')

data = {}
data['html_url'] = []
for repo in r.json():
    if not repo['private']:
        data['html_url'].append(repo['html_url'])

with open('data.json', 'w') as f:
   json.dump(data, f)
