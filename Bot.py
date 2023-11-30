import telebot
from telebot import types
import Database

db = Database.DataAccessObject()

# token = 
bot = telebot.TeleBot(token)

# menu_mark = types.ReplyKeyboardMarkup(
#     one_time_keyboard=False, resize_keyboard=True, row_width=2)
# homework_mark = types.ReplyKeyboardMarkup(
#     one_time_keyboard=True, resize_keyboard=True, row_width=2)
# subject_mark = types.ReplyKeyboardMarkup(
#     one_time_keyboard=True, resize_keyboard=True, row_width=2)

# menu_btn1 = types.KeyboardButton("Расписание")
# menu_btn3 = types.KeyboardButton("Просмотр дз")
# menu_btn4 = types.KeyboardButton("Добавление дз")
# menu_btn5 = types.KeyboardButton("Изменение расписания")
# menu_mark.add(menu_btn1, menu_btn3, menu_btn4, menu_btn5)

# homework_btn2 = types.KeyboardButton("Добавление дз")
# homework_btn1 = types.KeyboardButton("Просмотр дз")
# homework_mark.add(homework_btn1, homework_btn2)

# subject_btn2 = types.KeyboardButton("Выберите предмет")
# subject_mark.add(subject_btn2)


@bot.message_handler(commands=['start'])
def start(message):
    db.DataUpdate()
    tmp = db.get_things()
    bot.send_message(message.from_user.id, str(tmp))


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

    # else:
    #     main.PrintDiscount()

def GetType(message):
    type = message.text
    print(db.get_thing(type))
    for name in db.get_thing(type):
        bot.send_message(message.from_user.id, str(name))
        print(name)
    # bot.send_message(message.from_user.id, db.get_thing(type))
    # bot.send_message(message.from_user.id, "Домашняя работа добавлена",
    #                  reply_markup=menu_mark)


bot.polling(none_stop=True, interval=0)
