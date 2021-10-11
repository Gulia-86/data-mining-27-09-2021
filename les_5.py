#Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.common import exceptions as se
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['db_mail']
base = db.letters

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://mail.ru/')

elem = driver.find_element(By.NAME, "login")
elem.send_keys("study.ai_172@mail.ru")
elem.send_keys(Keys.ENTER)
time.sleep(5)
elem = driver.find_element(By.NAME, "password")
elem.send_keys('NextPassword172???')
elem.send_keys(Keys.ENTER)
time.sleep(10)

hrefs = []
while True:
    try:
        #собираем ссылки на письма
        items = driver.find_elements(By.XPATH, "//a[contains(@class, 'letter')]")
        for item in items:
            hrefs.append(item.get_attribute('href'))
        #это не сработало - driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #просто листаем вниз
        item.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    except se.ElementNotInteractableException:
        break
hrefs = set(hrefs)
all_letters = []

#заходим в каждое письмо по ссылке
for href in hrefs:
        driver.get(href)
        time.sleep(3)
        letters = {}
        #от кого
        correspondent = driver.find_element(By.XPATH, ".//span[@class = 'letter-contact']").text
        #дата отправки
        item_date = driver.find_element(By.XPATH, ".//div[@class = 'letter__date']").text
        #тема письма
        theme = driver.find_element(By.XPATH, ".//h2[@class = 'thread__subject']").text
        #текст письма полный
        content = driver.find_element(By.XPATH, "//div[@class='letter-body__body']").text

        letters['correspondent'] = correspondent
        letters['item_date'] = item_date
        letters['theme'] = theme
        letters['content'] = content
        letters['link'] = href
        all_letters.append(letters)
        try:
            base.update_one({'link': letters['link']}, {'$set': letters}, upsert=True)
        except Exception as exc:
            print('Что-то пошло не так/n', exc)
            continue

pprint(all_letters)
