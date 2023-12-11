#Сopyright © 2023 Serikov Artur Aleksandrovich
#Contact Email: artueserikov3986@gmail.com

#Импорт библиотек:
import telebot, configparser


#Переменные:
run = True


#Чтение файла конфигурации
config = configparser.ConfigParser()
config.read('config.ini')
token = config["Private"]["token"] #Присваиваем токен переменной


#Код самого бота:
bot = telebot.TeleBot(token) #Создаем бота

#Ответ на /start
@bot.message_handler(commands=['start']) #Условия запуска функции
def start(message): #Функция, которая будем выполнена при условии выше
    bot.send_message(message.chat.id, 'Привет! Бот пока в разработке. Жди)')






bot.polling(non_stop=run) #Для постоянной работы бота
#Soon....