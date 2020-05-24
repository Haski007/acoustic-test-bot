# -*- coding: utf-8 -*-

import os
from telebot import types

def call_handler(call, bot):
	keyboard = types.InlineKeyboardMarkup()

	# Buttons set
	main_button = types.InlineKeyboardButton(text="\U0001F3E0 To main menu", callback_data="mainmenu")
	keyboard.add(main_button)

	text_to_generate = "\t/generate - to generate white noise. Flags:\n"\
		"\t\t\t-rate\t\t\tto set custom bitrate\n" \
		"\t\t\t-bits\t\t\tto set custom sample rate\n" \
		"\t\t\t-duration\t\t\tto set custom duration of audio file\n"

	bot.edit_message_text(chat_id=call.message.chat.id,
						  message_id=call.message.message_id,
						  text=text_to_generate,
						  reply_markup=keyboard)

def create_command(command):
	res = "." + command
	return res


def get_white_noise(message):
	cmd = create_command(message.text)

	# Use my Golang generator
	os.system(cmd)

	for file in os.listdir("."):
		if file.endswith(".wav"):
			return open(file, 'rb')


def remove_audio_files():
	for file in os.listdir("."):
		if file.endswith(".wav"):
			os.remove(file)
