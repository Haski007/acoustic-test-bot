#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telebot import types

def get_table_name(table):
	if table == 'external':
		return 'Розрахунок можливості існування акустичного каналу витоку інформації для Зовнішньої стіни'
	elif table == 'partitions':
		return 'Розрахунок можливості існування акустичного каналу витоку інформації для офісних перегородок'
	elif table == 'floor':
		return 'Розрахунок можливості існування акустичного каналу витоку інформації для Сідлоги'
	elif table == 'ceiling':
		return 'Розрахунок можливості існування акустичного каналу витоку інформації для Стелі'
	elif table == 'windows':
		return 'Розрахунок можливості існування акустичного каналу витоку інформації для Вікон'
	elif table == 'doors':
		return 'Розрахунок можливості існування акустичного каналу витоку інформації для Дверей'

def parse(call, bot):

	filename = str("./resources/" + call.data + ".png")

	file = open(filename, 'rb')

	bot.send_photo(chat_id=call.message.chat.id, photo=file)
	file.close()

	# Set keyboard
	keyboard = types.InlineKeyboardMarkup()
	back_button = types.InlineKeyboardButton(text="\U00002196 Back", callback_data='tables')
	main_button = types.InlineKeyboardButton(text="\U0001F3E0 To main menu", callback_data="mainmenu")
	keyboard.add(back_button, main_button)
	bot.send_message(chat_id=call.message.chat.id, text=get_table_name(call.data), reply_markup=keyboard)
