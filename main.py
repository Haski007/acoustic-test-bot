# -*- coding: utf-8 -*-
import os

import telebot
from telebot import types

import Calculations
import config
import Generator
import Messages
import Tables

bot = telebot.TeleBot(config.TOKEN)

print(bot.get_me())

def log(message, answer):
	print("\n-----------")
	from datetime import datetime
	print(datetime.now())
	print("Message from {0} {1}. (id = {2})\nText - {3}".format(message.from_user.first_name,
																 message.from_user.last_name,
																 str(message.from_user.id),
																message.text))
	print("Answer:", answer)

# on different commands - answer in Telegram

#################################### START #################################

@bot.message_handler(commands=["start"])
def start_handler(message):
	"""Send a message when the command /start is issued."""
	keyboard_main = types.InlineKeyboardMarkup(row_width=2)

	# Buttons set
	tables_button = types.InlineKeyboardButton(text="Tables", callback_data="tables")
	calc_button = types.InlineKeyboardButton(text="Calculations", callback_data="calculations")
	generator_button = types.InlineKeyboardButton(text="Noize Generator", callback_data="generator")
	keyboard_main.add(tables_button, calc_button, generator_button)

	bot.send_message(message.chat.id, "Choose your destiny...", reply_markup=keyboard_main)

	log(message, "Start menu")


#################################### HELP #################################

@bot.message_handler(commands=["help"])
def help(message):
	"""Send a message when the command /help is issued."""
	answer = Messages.help(message)
	bot.send_message(message.chat.id, answer)
	log(message, "Help stuff!")





#################################### GENERATE #################################
# generate command generates white_noise audio file and send it back
@bot.message_handler(commands=["generate"])
def generate_handler(message):
	bot.send_message(message.chat.id, "Generating...")

	bot.send_message(message.chat.id, "Done. Here is your noise!")
	bot.send_audio(message.chat.id, Generator.get_white_noise(message))


	Generator.remove_audio_files()
	log(message, "Created noise file cmd = '{0}'!".format(message.text))



#################################### Calculation handlers #####################################
@bot.message_handler(commands=["obtacle_passing"])
def obracle_passing_handler(message):
	answer = Calculations.obtacle_passing(message)
	bot.send_message(chat_id=message.chat.id, text=answer)
	log(message, answer)


#################################### Handle all messages ##############################
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
	log(message, "Chtoto napisal")


################################### CALLBACKS #########################################
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.data == "mainmenu":
		keyboard_main = types.InlineKeyboardMarkup(row_width=2)

		# Buttons set
		tables_button = types.InlineKeyboardButton(text="Tables", callback_data="tables")
		calc_button = types.InlineKeyboardButton(text="Calculations", callback_data="calculations")
		keyboard_main.add(tables_button, calc_button)

		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
							  text="Choose your destiny...", reply_markup=keyboard_main)

	elif call.data == "generator":
		Generator.call_handler(call, bot)

	elif call.data == "tables":
		keyboard = types.InlineKeyboardMarkup()

		# Buttons set
		external_button = types.InlineKeyboardButton(text="External wall", callback_data="external")
		partitions_button = types.InlineKeyboardButton(text="Wall partitions", callback_data="partitions")
		floor_button = types.InlineKeyboardButton(text="Floor", callback_data="floor")
		ceiling_button = types.InlineKeyboardButton(text="Сeiling", callback_data="ceiling")
		windows_button = types.InlineKeyboardButton(text="Windows", callback_data="windows")
		doors_button = types.InlineKeyboardButton(text="Doors", callback_data="doors")
		main_button = types.InlineKeyboardButton(text="\U0001F3E0 To main menu", callback_data="mainmenu")
		keyboard.add(external_button, partitions_button, floor_button, ceiling_button, windows_button, doors_button, main_button)

		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="There are such tables:",
							  reply_markup=keyboard)
	elif call.data == "calculations":
		Calculations.call_handler(call, bot)

	##################################### ADDITIONAL LEVEL: Tables ################################################
	elif call.data == "external" or call.data == "partitions" or call.data == "floor" or call.data == "ceiling" or call.data == "windows" or call.data == "doors":
		Tables.parse(call, bot)


if __name__ == '__main__':
	bot.polling(none_stop=True)
