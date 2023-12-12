#Сopyright © 2023 Serikov Artur Aleksandrovich
#Contact Email: artueserikov3986@gmail.com

#Импорт библиотек:
import telebot, configparser, requests
from bs4 import BeautifulSoup
from PIL import Image

#Чтение файла конфигурации
config = configparser.ConfigParser()
config.read('Config.ini')
token = config["Private"]["token"] #Присваиваем токен переменной
url = config["Private"]["url"] #Присваиваем url переменной


#Переменные:
run = True


#Функция ниже предназначена для парсинга сайта
#Она ищет все ссылки и мы выбираем нужные из них
#Данные ссылки используются для скачивания изображения с сайта

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
            img = (link.get('src')) #(link.get('src')) - фильтр
            print (img)
    return(img)

Pars() #Вызов парсера


#Код самого бота:
bot = telebot.TeleBot(token) #Создаем бота

#Ответ на /start
@bot.message_handler(commands=['start']) #Условия запуска функции
def start(message): #Функция, которая будем выполнена при условии выше
    bot.send_message(message.chat.id, 'Привет!')
    print("Старт")

#Обработка обычного текста
@bot.message_handler()
def akk_message(message):
    #Отправка изображения по текстовому запросу:
    if message.text.lower() == "расписание" or "распорядок" or "пары" or "занятия":
        schedule = open("schedule.jpg", "rb")
        bot.send_message(message.chat.id, "Расписание на 12 декабря")
        bot.send_photo(message.chat.id, schedule)

    #Отправка ссылки на сайт по текстовому запросу:
    elif message.text.lower() == "сайт" or "site" or "website" or "вебсайт":
        bot.send_message(message.chat.id, "cайт")
    else:
        pass



bot.polling(non_stop=run) #Для постоянной работы бота
#Soon....