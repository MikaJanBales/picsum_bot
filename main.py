import fileinput
import re
import requests
import telebot
import json
import csv
import ast

TOKEN = '6080161304:AAGX73pAvXF87SQzZd-WGH_CyXfDRT8whzc'

bot = telebot.TeleBot(TOKEN)


def check_uri(uri):
    check = re.fullmatch('https://picsum.photos/v2/list(?:\?page=(\d+))?(?:&limit=(\d+))?', uri)
    return True if check else False


def search_photo(num_id):
    with open("info.txt", "r") as f:
        for line in f:
            data = ast.literal_eval(line)
            if data["id"] == num_id:
                break
    return data


def save_info_photo(uri):
    response_info_all_photo = requests.get(uri.text)
    if response_info_all_photo.status_code == 200:
        info_all_photo = json.loads(response_info_all_photo.content)
        for info_photo in info_all_photo:
            path_file_info = f"info.txt"
            with open(path_file_info, "a") as f:
                arg = f"{str(info_photo)}\n"
                f.write(arg)


@bot.message_handler(commands=["start"])
def start(message):
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
        delete_photo(callback.message, info[1])


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
        names = ['id', 'author', 'width', 'height', 'url', 'download_url']
        file_writer = csv.DictWriter(w_file, delimiter=",", lineterminator="\r", fieldnames=names)
        file_writer.writeheader()

        with open("info.txt", mode="r") as f:
            for line in f:
                data = ast.literal_eval(line)
                file_writer.writerow(data)

    with open("table_info_photo.csv", "rb") as doc:
        bot.send_document(message.chat.id, doc)

    mess = "Таблица с изображениями успешно сформирована"
    bot.send_message(message.chat.id, mess, reply_markup=menu_photo())


def look_list_photo(message):
    mess = "Список фотографий."
    markup = telebot.types.InlineKeyboardMarkup()
    with open("info.txt", mode="r") as f:
        for line in f:
            data = ast.literal_eval(line)
            number_id = data["id"]
            author = data["author"]
            btn = telebot.types.InlineKeyboardButton(f"{author} ({number_id})",
                                                     callback_data=f"get_photo:{number_id}")
            markup.row(btn)
    bot.send_message(message.chat.id, mess, reply_markup=markup)


def get_photo(message, num_id):
    data = search_photo(num_id)
    mess = f"Author: {data['author']}\nID: {num_id}\nSize: {data['width']}x{data['height']}\nURL: {data['url']}\nDownload URL: {data['download_url']}"

    markup = telebot.types.InlineKeyboardMarkup()
    btn_del = telebot.types.InlineKeyboardButton('Удалить',
                                                 callback_data=f"check_delete_photo:{num_id}")
    markup.row(btn_del)
    btn_back = telebot.types.InlineKeyboardButton('Назад', callback_data='look_list_photo')
    markup.row(btn_back)
    bot.send_photo(message.chat.id, data['download_url'])
    bot.send_message(message.chat.id, mess, reply_markup=markup)


def check_delete_photo(message, num_id):
    data = search_photo(num_id)
    mess = f"Вы уверены, что хотите удалить эту фотографию?\n{data['author']} ({num_id})"
    markup = telebot.types.InlineKeyboardMarkup()
    btn_yes = telebot.types.InlineKeyboardButton('Да',
                                                 callback_data=f"delete_photo:{num_id}")
    btn_no = telebot.types.InlineKeyboardButton('Нет', callback_data='look_list_photo')
    markup.row(btn_yes, btn_no)
    bot.send_photo(message.chat.id, data['download_url'])
    bot.send_message(message.chat.id, mess, reply_markup=markup)


def delete_photo(message, num_id):
    for line in fileinput.input('info.txt', inplace=True):
        data = ast.literal_eval(line)
        if data["id"] == num_id:
            continue  # пропускаем строку с нужным id
        print(line.rstrip())

    mess = "Фотография была успешна удалена."
    bot.send_message(message.chat.id, mess, reply_markup=look_list_photo(message))


bot.polling(none_stop=True)
