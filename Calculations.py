# -*- coding: utf-8 -*-

from telebot import types
import math

def get_args(text):
	res = str(text).split(sep=" ")
	return res

def call_handler(call, bot):
	keyboard = types.InlineKeyboardMarkup()

	# Buttons set
	main_button = types.InlineKeyboardButton(text="\U0001F3E0 To main menu", callback_data="mainmenu")
	keyboard.add(main_button)

	formulas = """Щоб зробити розрахунки:
	/obtacle_passing [уровень шума до преграды] [площа перешкоди] [ізоляція повітряного шуму] [поправка в Дб]
	(порахую рівень шуму мови при проходженні через перешкоду.)"""

	bot.edit_message_text(chat_id=call.message.chat.id,
						  message_id=call.message.message_id,
						  text=formulas,
						  reply_markup=keyboard)

def obtacle_passing(message):
	args = get_args(message.text)
	try:
		L0 = float(args[1])
		S = float(args[2])
		R = float(args[3])
		d = float(args[4])
		L = L0 + 10 * math.log10(S) - R - d

		return L
	except:
		return "ArgsError"






