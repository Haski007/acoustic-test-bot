# -*- coding: utf-8 -*-
import os
import urllib.request

import Config


def download_voice(message, file_url):
	direct = "voices/" + message.from_user.first_name + "/"

	if not os.path.exists(direct):
		os.mkdir(direct)


	urllib.request.urlretrieve(file_url, direct + str(message.voice.file_id))
