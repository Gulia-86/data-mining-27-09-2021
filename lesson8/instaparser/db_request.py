from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
mongo_base = client['instagram']
collection = mongo_base['instaparse']

#objects = collection.find({'relation': "follower"})          # возвращает подписчиков
objects = collection.find({'relation': 'following'})        # возвращает подписки
pprint(list(objects))