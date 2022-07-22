# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random

import telebot

import telebot
import os
from telebot import types

bot = telebot.TeleBot('')

general_markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
generalbtn_1 = types.KeyboardButton('Продать аккаунты ✅')
generalbtn_2 = types.KeyboardButton('Купить аккаунты 💰')
generalbtn_3 = types.KeyboardButton('О боте ℹ')
general_markup.add(generalbtn_1, generalbtn_2, generalbtn_3)
admin_chat_id = ''
admin_username = ''
currency = 'р'
requisites = ''

trade_markup = types.ReplyKeyboardMarkup(row_width=2)
tradebtn_1 = types.KeyboardButton('Выход ❎')
trade_markup.add(tradebtn_1)

account_types = {}
current_checking = {}

def load_accounts():
    for folder in os.listdir('accounts'):
        if 'txt' in folder:
            try:
                with open(f'accounts/{folder}') as f:
                        first_line = f.read().splitlines()[0]
                    # first_line = ''
                    # for part in f.read().splitlines()[0].split(' ')[:-1]:
                    #     first_line += part
                account_types[first_line.replace(f' {first_line.split(" ")[-1]}', '')] = folder
            except:
                pass
    with open ('requisites.txt') as f:
        global requisites
        for line in f.readlines():
            requisites += line

@bot.message_handler(regexp='chat_id')
def get_chat_id(message):
    if message.from_user.username != admin_username:
        return
    bot.send_message(message.chat.id, message.chat.id)

@bot.message_handler(regexp='О боте ℹ')
def bot_info(message):
    bot.send_message(message.chat.id, 'Телеграм бот для покупки аккаунтов\nТс ')

@bot.message_handler(regexp='Выход')
def command_exit(message):
    start_command(message)

@bot.message_handler(regexp='Купить аккаунты 💰')
def buy_tokens(message):
    account_types_to_buy = ''
    for account_type in account_types.keys():
        with open(f'accounts/{account_types[account_type]}') as f:
            price = f.readlines()[0].split(' ')[-1]
        account_types_to_buy += f'{account_type} {price[:-1]}{currency}\n'
    bot.send_message(message.chat.id, f'{account_types_to_buy}',
                                      reply_markup=trade_markup)
    bot.send_message(message.chat.id, f'Для покупки используйте команду "ba [имя] [количество]\nпример: ba simple_account 100')

@bot.message_handler(regexp='Продать аккаунты')
def sell_tokens(message):
    bot.send_message(message.chat.id, f'Отправьте txt документ с аккаунтами и мы с вами свяжемся.',
                                       reply_markup=trade_markup)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.username} ✋\nИспользуя этот бот вы можете покупать и продавать аккаунты 💰', reply_markup=general_markup)

@bot.message_handler(regexp='ba')
def buying_process(message):
    number = int(message.text.split(' ')[-1])
    account_name = message.text
    account_name = account_name.split('ba ')[1]
    account_name = account_name.split(f' {str(number)}')[0]
    try:
        account_types[account_name]
    except KeyError:
        bot.send_message(message.chat.id, f'Извините, этих аккаунтов нет в наличии')
        return
    with open(f'accounts/{account_types[account_name]}') as f:
        counter = len(f.readlines()) - 1
        if counter < number:
            bot.send_message(message.chat.id, 'Извините, этих аккаунтов нет в наличии')
            return
    with open(f'accounts/{account_types[account_name]}') as f:
                accounts = (f.readlines()[1:number + 1])
    with open(f'accounts/{account_types[account_name]}', 'r') as source:
        to_write = []
        lines = source.readlines()
        to_write.append(lines[0])
        for line in lines[number + 1:]:
            to_write.append(line)
    with open(f'accounts/{account_types[account_name]}', 'w') as dest:
        dest.writelines(to_write)
    order_id = random.randint(10000,99999)
    with open(f'{order_id}.txt', 'w') as f:
        f.write(f'{message.chat.id}\n {account_name}\n')
        f.writelines(accounts)
    with open(f'accounts/{account_types[account_name]}') as f:
        price = f.readlines()[0].split(' ')[-1]
    to_pay = int(price) * number
    bot.send_message(message.chat.id, f'Ваш номер заказа {order_id}✅. Цена: {to_pay}{currency}\n реквизиты для оплаты: {requisites}')
    bot.send_message(admin_chat_id, f'{order_id} {account_name} 📝\n к оплате {to_pay}{currency}\n accept_buy [номер заказа] если вы получили оплату ✅\n decline_buy [номер заказа] если вы не получили оплату ❌')

@bot.message_handler(content_types=['document'])
def selling_process(message):
    sell_id = random.randint(10000,99999)
    file_id = message.document.file_id
    bytes_file = bot.download_file(bot.get_file(file_id).file_path)
    with open(f'selling/{sell_id}.txt', 'wb') as f:
        f.write(bytes_file)
    with open(f'selling/{sell_id}.txt', 'a') as f:
        f.write(f'{message.from_user.username}\n')
    bot.send_message(admin_chat_id, f'{message.from_user.username} хочет продать вам аккаунты💰')
    with open(f'selling/{sell_id}.txt', 'rb') as f:
        bot.send_document(admin_chat_id, f)
    bot.send_message(message.chat.id, 'Успешно')

@bot.message_handler(regexp='accept_buy')
def accept_buy(message):
    if message.from_user.username != admin_username:
        return
    order_id = message.text.split(' ')[1]
    with open(f'{order_id}.txt') as f:
        chat_id = f.readlines()[0]
    with open(f'{order_id}.txt', 'r') as source:
        to_write = source.readlines()[2:]
    with open(f'{order_id}.txt',  'w') as dest:
        dest.writelines(to_write)
    with open(f'{order_id}.txt', 'rb') as f:
        bot.send_document(chat_id, f)
    bot.send_message(message.chat.id, 'Успешно')

@bot.message_handler(regexp='decline_buy')
def decline_buy(message):
    if message.from_user.username != admin_username:
        return
    order_id = message.text.split(' ')[1]
    with open(f'{order_id}.txt') as f:
        accounts = f.readlines()[2:]
    with open(f'{order_id}.txt') as f:
        account_name = f.readlines()[1]
    account_name = account_name[1:-1]
    f_n = open(f'accounts/{account_types[account_name]}', 'a')
    for account in accounts:
        f_n.write(account)
    bot.send_message(message.chat.id, 'Успешно')




while True:
    try:
        load_accounts()
        bot.polling()
    except:
        pass
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
