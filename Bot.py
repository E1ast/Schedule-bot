#Сopyright © 2023 Serikov Artur Aleksandrovich
#Contact Email: artueserikov3986@gmail.com

#Импорт библиотек:
import telebot, configparser, requests, wget, os
from bs4 import BeautifulSoup
from PIL import Image

#Чтение файла конфигурации
config = configparser.ConfigParser()
config.read('Config.ini')
token = config["Private"]["token"] #Присваиваем токен переменной
url = config["Private"]["url"] #Присваиваем url переменной
dir = os.getcwd() #Узнаем текущую директорию
print(f"\nТекущая директория: {dir}")

#Переменные:
run = True


#Функция ниже предназначена для парсинга сайта и скачивания изображения
#Она ищет все ссылки и мы выбираем нужные из них
#Данные ссылки используются для скачивания изображения с сайта

@staticmethod
def Pars():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    links = soup.find_all('img') #Фильтр

    Counter = 0 #Сброс переменной счетчика
    for link in links: 
        links_all = link.get('src')
        Counter += 1 #Счетчик
        if Counter == 4: #Принтим 4-ый элемент
            img_url = (link.get('src')) #(link.get('src')) - фильтр
            print (f"Текущая активная ссылка: {img_url}")
    if (os.path.exists('schedule.jpg')) == False:
        wget.download(img_url, 'schedule.jpg')
    else:
        print(f"Если вы хотите обновить изображение, то удалите schedule.jpg и перезапустите программу")

Pars() #Вызов парсера


#Код самого бота:
bot = telebot.TeleBot(token) #Создаем бота
print("\n\nБот запущен!\n\nСобытия:")

#Ответ на /start
@bot.message_handler(commands=['start']) #Условия запуска функции
def start(message): #Функция, которая будем выполнена при условии выше
    bot.send_message(message.chat.id, 'Привет!')
    print("Кто-то использовал /start")

#Ответ на /расписание
@bot.message_handler(commands=['расписание']) #Условия запуска функции
def schedule(message): #Функция, которая будем выполнена при условии выше
    schedule = open("schedule.jpg", "rb")
    bot.send_message(message.chat.id, "Актуальное расписание:")
    bot.send_photo(message.chat.id, schedule)
    print("Кто-то решил узнать расписание")

#Ответ на /start
@bot.message_handler(commands=['start']) #Условия запуска функции
def start(message): #Функция, которая будем выполнена при условии выше
    bot.send_message(message.chat.id, 'Привет!')
    print("Кто-то использовал /start")

#Обработка обычного текста
@bot.message_handler()
def akk_message(message):
    #Отправка изображения по текстовому запросу:
    if message.text.lower() == "расписание" or "распорядок" or "пары" or "занятия":
        schedule = open("schedule.jpg", "rb")
        bot.send_message(message.chat.id, "Актуальное расписание:")
        bot.send_photo(message.chat.id, schedule)
        print("Кто-то решил узнать расписание")

    #Отправка ссылки на сайт по текстовому запросу:
    elif message.text.lower() == "сайт" or "site" or "website" or "вебсайт":
        bot.send_message(message.chat.id, "http://simfpolyteh.ru/raspisanie/")
        print("Кто-то решил зайти на сайт колледжа")
    else:
        bot.send_message(message.chat.id, "Такой команды нет :/")
        print("Кто-то ввел команду неправильно")



bot.polling(non_stop=run) #Для постоянной работы бота
#Soon....