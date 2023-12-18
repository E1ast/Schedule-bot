#Сopyright © 2023 Serikov Artur Aleksandrovich
#Contact Email: artueserikov3986@gmail.com

#Импорт библиотек:
import telebot, configparser, requests, wget, os, sys, time
from bs4 import BeautifulSoup
from PIL import Image
from telebot import types



#Чтение файла конфигурации
config = configparser.ConfigParser()
config.read('Config.ini')
token = config["Main"]["token"] #Присваиваем токен переменной
url = config["Main"]["url"] #Присваиваем url переменной
about_lang = config["Lang"]["about"] #Текст вывода команды /about
help_lang = config["Lang"]["help"] #Текст вывода команды /help
schedule_lang = config["Lang"]["schedule"] #Текст вывода команды /schedule
about_img = config["Lang"]["img"] #Текст вывода команды /img
bell_lang = config["Lang"]["bell"] #Текст вывода команды /bell
img_lang = config["Lang"]["img"] #Текст вывода команды
cmd_error_lang = config["Lang"]["cmd_error"] #Текст вывода ошибки из-за неправильной команды



#Узнаем текущую директорию
dir = os.getcwd()
print(f"\nТекущая директория: {dir}")

#Переменные:
bot_run = True
named_tuple = time.localtime()
time_full = time.strftime("%m.%d.%Y, %H:%M:%S", named_tuple) #Текущая дата и время
time = time.strftime("%H:%M:%S", named_tuple) #Текущая дата и время

#Функция перезагрузки программы
def Restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)



#Функция ниже предназначена для парсинга сайта и скачивания изображения
#Она ищет все ссылки и мы выбираем нужные из них
#Данные ссылки используются для скачивания изображения с сайта

@staticmethod
def Pars():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    links = soup.find_all('img') #Фильтр

    counter = 0 #Сброс переменной счетчика
    for link in links: 
        links_all = link.get('src')
        counter += 1 #Счетчик
        if counter == 4: #Принтим 4-ый элемент
            schedule_url = (link.get('src')) #(link.get('src')) - фильтр
            print (f"Текущая активная ссылка расписание пар: {schedule_url}")
        elif counter == 5:
            bell_url = (link.get('src'))
            print (f"Текущая активная ссылка расписание звонков: {bell_url}")
        else:
             pass


    #Логирование и сохранение старых расписаний пар
    if (os.path.exists('schedule.jpg')) == False:
        wget.download(schedule_url, 'schedule.jpg') #Скачивание файла
    else:
        os.rename('schedule.jpg', f"logs_schedule/schedule_{time_full}.jpg") #Перемещение файла в папку логов
        Pars()
    
Pars() #Вызов парсера



#Код самого бота:
bot = telebot.TeleBot(token) #Создаем бота
print("\n\nБот запущен!\n\nСобытия:")

#Кнопки
markup_keyboard = types.ReplyKeyboardMarkup()
markup_message = types.InlineKeyboardMarkup()
markup_message.add(types.InlineKeyboardButton('Перейти', url = url))
btn1 = types.KeyboardButton('Узнать расписание пар')
btn2 = types.KeyboardButton('Узнать расписание звонков')
btn3 = types.KeyboardButton('Помощь')
btn4 = types.KeyboardButton('О боте')
btn5 = types.KeyboardButton('Сайт')

markup_keyboard.row(btn3, btn4, btn5)
markup_keyboard.row(btn2)
markup_keyboard.row(btn1)



#Ответы на команды

#Ответ на /start
@bot.message_handler(commands=['start']) #Условия запуска функции
def Start(message): #Функция, которая будем выполнена при условии выше
    bot.send_message(message.chat.id, 'Привет!', reply_markup=markup_keyboard)
    print(f"[{time}] {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username}): использовал /start")


@bot.message_handler(commands=['reload']) #Условия запуска функции
def Start(message): #Функция, которая будем выполнена при условии выше
    Pars()
    bot.send_message(message.chat.id, 'Обновлено!', reply_markup=markup_keyboard)
    print(f"[{time}] {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username}): обновил данные")

#Ответ на /расписание
@bot.message_handler(commands=['расписание','schedule','пары']) #Условия запуска функции
def Schedule(message): #Функция, которая будем выполнена при условии выше
    schedule = open("schedule.jpg", "rb")
    bot.send_message(message.chat.id, schedule_lang)
    bot.send_photo(message.chat.id, schedule)
    print(f"[{time}] {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username}): решил узнать расписание пар")

#Ответ на /сайт
@bot.message_handler(commands=['site','сайт']) #Условия запуска функции
def Site(message): #Функция, которая будем выполнена при условии выше
        bot.send_message(message.chat.id, url, reply_markup=markup_message)
        print(f"[{time}] {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username}): зайти на сайт колледжа")

@bot.message_handler(commands=['помошь','help','Помощь','Help']) #Условия запуска функции
def Help(message): #Функция, которая будем выполнена при условии выше
        bot.send_message(message.chat.id, text = help_lang, parse_mode = 'html')
        print(f"[{time}] {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username}): воспользовался помощью")

@bot.message_handler(commands=['about']) #Условия запуска функции
def About(message): #Функция, которая будем выполнена при условии выше
        bot.send_message(message.chat.id, about_lang, parse_mode = 'html')
        print(f"[{time}] {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username}): решил подробнее узнать о боте")

@bot.message_handler(commands=['bell']) #Условия запуска функции
def Bell(message): #Функция, которая будем выполнена при условии выше
    bell = open("bell.jpg", "rb")

    bot.send_message(message.chat.id, bell_lang)
    bot.send_photo(message.chat.id, bell)
    print(f"[{time}] {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username}): решил узнать расписание звонков")

#Обработка получения фото
@bot.message_handler(content_types=['photo'])
def Get_Photo(message):
    bot.reply_to(message, img_lang)
    print(f"[{time}] {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username}): скинул боту фотку")




#Обработка обычного текста
@bot.message_handler()
def Simple_message(message):
    #Отправка изображения по текстовому запросу:
    if message.text.lower() == "узнать расписание звонков":
        Bell(message)

    elif message.text.lower() == "узнать расписание пар":
        Schedule(message)

    #Отправка ссылки на сайт по текстовому запросу:
    elif message.text.lower() == "сайт":
        Site(message)

    elif message.text.lower() == "помощь":
        Help(message)

    elif message.text.lower() == "о боте":
        About(message)

    else:
        bot.send_message(message.chat.id, "Такой команды нет :/")
        print(f"[{time}] {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username}): ввел команду неправильно: {message.text}")



bot.polling(non_stop=bot_run) #Для постоянной работы бота

#Soon....