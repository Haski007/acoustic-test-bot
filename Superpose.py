import os
import shutil

from pydub import AudioSegment
from os import listdir



def combine(message):
	sounds_path = "voices/" + message.from_user.first_name + "/"

	sounds = []
	try:
		for file_name in listdir(sounds_path):
			sounds.append(AudioSegment.from_file(sounds_path + file_name))
	except:
		return ""

	if len(sounds) > 0:
		combined = sounds[0]
	else:
		return ""

	for sound in sounds:
		combined = combined.overlay(sound)

	combined.export(sounds_path + "Superimposed.wav", format='wav')
	return sounds_path

def remove(path, user):
	archive_path = "voices/archive/"


	for file in os.listdir(path):
		if not os.path.exists(archive_path + user):
			os.mkdir(archive_path + user)
		if file == "Superimposed.wav":
			os.remove(path + file)
		else:
			shutil.move(path + file, archive_path + user)

	# Check overfilling

	while len(os.listdir(archive_path + user)) > 50:
		os.remove(archive_path + user + "/" + os.listdir(archive_path + user)[len(os.listdir(archive_path + user)) - 1])
