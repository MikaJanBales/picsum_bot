import re
import requests
import telebot
import json
import csv

from db import delete_photo, get_list_photo, get_id_and_author_photo, \
    get_info_photo, add_photo, create_table

TOKEN = '6080161304:AAGX73pAvXF87SQzZd-WGH_CyXfDRT8whzc'

bot = telebot.TeleBot(TOKEN)


# Проверка отправленной ссылки
def check_uri(uri):
    check = re.fullmatch('https://picsum.photos/v2/list(?:\?page=(\d+))?(?:&limit=(\d+))?', uri)
    return True if check else False


def save_info_photo(uri):
    response_info_all_photo = requests.get(uri.text)
    if response_info_all_photo.status_code == 200:
        info_all_photo = json.loads(response_info_all_photo.content)
        for info_photo in info_all_photo:
            add_photo(info_photo)


@bot.message_handler(commands=["start"])
def start(message):
    create_table()
    mess = 'Привет, это онбординг. Пришлите мне ссылку на список фотографий с picsum.photos, например: https://picsum.photos/v2/list?page=2&limit=100'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=["text"])
def get_user_uri(message):
    if check_uri(message.text):
        save_info_photo(message)
        mess = 'Фотографии успешно сохранены.'
        bot.send_message(message.chat.id, mess)
        bot.send_message(message.chat.id, 'Main menu', reply_markup=menu_photo())
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("Меню", callback_data="menu"))
        mess = 'Ссылка некорректна. Вы можете добавить фотографии из меню по кнопке ниже.'
        bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "menu":
        bot.send_message(callback.message.chat.id, 'Main menu', reply_markup=menu_photo())
    elif callback.data == "add_photo":
        mess = 'Пришлите мне ссылку на список фотографий с picsum.photos, например: https://picsum.photos/v2/list?page=2&limit=100'
        bot.send_message(callback.message.chat.id, mess)
    elif callback.data == 'look_list_photo':
        look_list_photo(callback.message)
    elif callback.data == 'table_csv_photo':
        make_table_csv(callback.message)
    elif callback.data.startswith("get_photo"):
        info = callback.data.split(":")
        get_photo(callback.message, info[1])
    elif callback.data.startswith("check_delete_photo"):
        info = callback.data.split(":")
        check_delete_photo(callback.message, info[1])
    elif callback.data.startswith("delete_photo"):
        info = callback.data.split(":")
        delete_photo(info[1])

        mess = "Фотография была успешно удалена."
        bot.send_message(callback.message.chat.id, mess, reply_markup=look_list_photo(callback.message))


def menu_photo():
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton('Добавить фотографии', callback_data='add_photo')
    markup.row(btn1)
    btn2 = telebot.types.InlineKeyboardButton('Список фоторграфий', callback_data='look_list_photo')
    markup.row(btn2)
    btn3 = telebot.types.InlineKeyboardButton('Получить таблицу фото', callback_data='table_csv_photo')
    markup.row(btn3)
    return markup


def make_table_csv(message):
    with open("table_info_photo.csv", mode="w", encoding="utf-8") as w_file:
        names = ['', 'ID', 'AUTHOR', 'WIDTH', 'HEIGHT', 'URL', 'DOWNLOAD_URL']
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow(names)

        data = get_list_photo()

        for info in data:
            file_writer.writerow(info)

    with open("table_info_photo.csv", "rb") as w_file:
        bot.send_document(message.chat.id, w_file)

    mess = "Таблица с изображениями успешно сформирована."
    bot.send_message(message.chat.id, mess, reply_markup=menu_photo())


def look_list_photo(message):
    mess = "Список фотографий."
    markup = telebot.types.InlineKeyboardMarkup()

    data = get_id_and_author_photo()

    for info in data:
        btn = telebot.types.InlineKeyboardButton(f"{info[1]} ({info[0]})", callback_data=f"get_photo:{info[0]}")
        markup.row(btn)

    bot.send_message(message.chat.id, mess, reply_markup=markup)


def get_photo(message, num_id):
    data = get_info_photo(num_id)
    mess = f"Author: {data[0][2]}\nID: {num_id}\nSize: {data[0][3]}x{data[0][4]}\nURL: {data[0][5]}\nDownload URL: {data[0][6]}"

    markup = telebot.types.InlineKeyboardMarkup()
    btn_del = telebot.types.InlineKeyboardButton('Удалить',
                                                 callback_data=f"check_delete_photo:{num_id}")
    markup.row(btn_del)
    btn_back = telebot.types.InlineKeyboardButton('Назад', callback_data='look_list_photo')
    markup.row(btn_back)
    bot.send_photo(message.chat.id, data[0][6])
    bot.send_message(message.chat.id, mess, reply_markup=markup)


def check_delete_photo(message, num_id):
    data = get_info_photo(num_id)
    mess = f"Вы уверены, что хотите удалить эту фотографию?\n{data[0][2]} ({num_id})"
    markup = telebot.types.InlineKeyboardMarkup()
    btn_yes = telebot.types.InlineKeyboardButton('Да',
                                                 callback_data=f"delete_photo:{num_id}")
    btn_no = telebot.types.InlineKeyboardButton('Нет', callback_data='look_list_photo')
    markup.row(btn_yes, btn_no)
    bot.send_photo(message.chat.id, data[0][6])
    bot.send_message(message.chat.id, mess, reply_markup=markup)


bot.polling(none_stop=True)
