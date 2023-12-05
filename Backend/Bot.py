import telebot
from telebot import types
import DataBase
    
db = DataBase.DataAccessObject()

token = "6906791170:AAFigjd2Hjh9x_vXzgEg3pf5MCiBGrg1Nw4"
bot = telebot.TeleBot(token)

menu_mark = types.ReplyKeyboardMarkup(
    one_time_keyboard=False, resize_keyboard=True, row_width=2)
homework_mark = types.ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True, row_width=2)
subject_mark = types.ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True, row_width=2)

menu_btn1 = types.KeyboardButton("Обновление данных")
menu_btn2 = types.KeyboardButton("Типы товаров")
menu_btn3 = types.KeyboardButton("Выбрать товар")
menu_mark.add(menu_btn1, menu_btn2, menu_btn3)


@bot.message_handler(commands=['start'])
def start(message):
    db.DataUpdate()
    tmp = db.get_things()
    bot.send_message(message.from_user.id, str(tmp), reply_markup=menu_mark)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    nickname = message.chat.username
    if message.text == "Обновление данных":
        db.DataUpdate()
        bot.send_message(message.from_user.id, 'Успешно')

    elif message.text == "Типы товаров":
        names = {}
        for name in db.get_things():
            names[name] = 1
        for key in names.keys():
            bot.send_message(message.from_user.id, key)

    elif message.text == "Выбрать товар":
        bot.send_message(message.from_user.id, "Введите название товара из типов товаров")
        bot.register_next_step_handler(message, GetType)

def GetType(message):
    type = message.text
    print(db.get_thing(type))
    for name in db.get_thing(type):
        bot.send_message(message.from_user.id, str(name))
        print(name)


bot.polling(none_stop=True, interval=0)
