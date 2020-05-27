# -*- coding: utf-8 -*-

import telebot
from telebot import types

import Calculations
import Config
import Generator
import Messages
import Superpose
import Tables
import Voices

bot = telebot.TeleBot(Config.DEV_TOKEN)

print(bot.get_me())

def log(message, answer):
	logs = "\n-----------\n"
	from datetime import datetime
	logs += str(datetime.now()) + "\n"
	logs += "Message from {0} {1}. (id = {2})\nText - {3}\n".format(message.from_user.first_name,
																 message.from_user.last_name,
																 str(message.from_user.id),
																message.text)
	if answer != "":
		logs += "Answer: " + answer

	print(logs)
	###########  write to file logs/bot.logs

	filename = str(datetime.now().date()) + ".log"
	f = open("logs/" + filename, 'a')
	f.write(logs)

# overload with call
def call_log(call, button):
	logs = "\n-----------\n"
	from datetime import datetime
	logs += str(datetime.now()) + "\n"
	logs += "Call from {0} {1}. (id = {2})\n\n".format(call.from_user.first_name,
																 call.from_user.last_name,
																 str(call.from_user.id))
	if button != "":
		logs += "Button: " + button

	print(logs)

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
	log(message, "Some help stuff!")





#################################### GENERATE #################################
# generate command generates white_noise audio file and send it back
@bot.message_handler(commands=["generate"])
def generate_handler(message):
	bot.send_message(message.chat.id, "Generating...")
	file = Generator.get_white_noise(message)
	bot.send_message(message.chat.id, "Done. Here is your noise!")
	bot.send_audio(message.chat.id, file)
	file.close()

	Generator.remove_audio_files()
	log(message, "Created noise file cmd = '{0}'!".format(message.text))

#################################### Superpose #################################
# generate command generates white_noise audio file and send it back
@bot.message_handler(commands=["superpose"])
def generate_handler(message):
	bot.send_message(message.chat.id, "Generating...")
	path = Superpose.combine(message)
	if path == "":
		bot.send_message(message.chat.id, "Error: there aren't enable voices!")
	else:
		file = open(path + "Superimposed.wav", 'rb')
		bot.send_message(message.chat.id, "Done. Here is your noise!")
		bot.send_audio(message.chat.id, file)
		file.close()
		Superpose.remove(path, message.from_user.first_name)

	log(message, "Created superimposed file for - {0}".format(message.from_user.first_name))



#################################### Calculation handlers #####################################
@bot.message_handler(commands=["obtacle"])
def obtacle_level_handler(message):
	answer = Calculations.obtacle_level(message)
	bot.send_message(chat_id=message.chat.id, text=answer)
	log(message, answer)


#################################### Handle voices #####################################
@bot.message_handler(func=lambda message: True, content_types=['voice'])
def voice_handler(message):
	Voices.download_voice(message, bot.get_file_url(message.voice.file_id))
	log(message, "Voice")

#################################### Handle all messages ##############################
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
	log(message, "")


################################### CALLBACKS #########################################
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.data == "mainmenu":
		keyboard_main = types.InlineKeyboardMarkup(row_width=2)

		# Buttons set
		tables_button = types.InlineKeyboardButton(text="Tables", callback_data="tables")
		calc_button = types.InlineKeyboardButton(text="Calculations", callback_data="calculations")
		generator_button = types.InlineKeyboardButton(text="Noize Generator", callback_data="generator")
		keyboard_main.add(tables_button, calc_button, generator_button)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
							  text="Choose your destiny...", reply_markup=keyboard_main)
		call_log(call, "Main menu")

	elif call.data == "generator":
		Generator.call_handler(call, bot)
		call_log(call, "Generator")

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

		call_log(call, "Tables")

	elif call.data == "calculations":
		Calculations.call_handler(call, bot)
		call_log(call, "Calculations")

	##################################### ADDITIONAL LEVEL: Tables ################################################
	elif call.data == "external" or call.data == "partitions" or call.data == "floor" or call.data == "ceiling" or call.data == "windows" or call.data == "doors":
		Tables.parse(call, bot)
		call_log(call, "Tables:{0}".format(call.data))



if __name__ == '__main__':
	bot.polling(none_stop=True)
