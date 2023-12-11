#Сopyright © 2023 Serikov Artur Aleksandrovich
#Contact Email: artueserikov3986@gmail.com

#Импорт библиотек
import requests, configparser
from bs4 import BeautifulSoup

#Чтение файла конфигурации
config = configparser.ConfigParser()
config.read('config.ini')
url = config["Private"]["url"] #Присваиваем токен переменной

run = True #Переменная для выключения бесконечного цикла


@staticmethod #Функция парсинга
def Pars():
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'lxml')

  links = soup.find_all('img') #Фильтр

  Counter = 0 #Сброс переменной счетчика
  for link in links: 
      links_all = link.get('src')
      Counter += 1 #Счетчик
      if Counter == 4: #Принтим 4-ый элемент
          print(link.get('src')) #(link.get('src')) - фильтр

#Бесконечный цикл проверки сайта:
while run:
  Pars() #Вызов парсера