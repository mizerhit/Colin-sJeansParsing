import telebot
from telebot import types
import model as model
from tokens import tg_token

db = model.DataAccessObject()


token = tg_token
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
menu_btn4 = types.KeyboardButton("все товары")
menu_mark.add(menu_btn1, menu_btn2, menu_btn3, menu_btn4)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Здравствуйте, я телеграм бот для поиска выгодных товаров на сайте colins.ru.", reply_markup=menu_mark)


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

    elif message.text == "все товары":
        bot.send_message(message.from_user.id, "Товары выведины в порядке от самой большой скидки к самой маленькой")
        for name in db.get_discount():
            bot.send_message(message.from_user.id, str(name).replace("(", "").replace(")", "").replace("'", "").replace(",", "  Цвет: ", 1).replace(",", "  Цена: ", 1).replace(",", "  Скидка: ", 1))
            print(name)
                
    elif message.text == "Выбрать товар":
        bot.send_message(message.from_user.id, "Введите название товара из типов товаров")
        bot.register_next_step_handler(message, GetType)


def GetType(message):
    type = message.text
    print(db.get_thing(type))
    for name in db.get_thing(type):
        bot.send_message(message.from_user.id, str(name).replace("(", "").replace(")", "").replace("'", "").replace(",", "  Цвет: ", 1).replace(",", "  Цена: ", 1).replace(",", "  Скидка: ", 1).replace(",", "  Фото: ", 1))
        print(name)

bot.polling(none_stop=True, interval=0)
