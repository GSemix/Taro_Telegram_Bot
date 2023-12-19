# -*- coding: utf-8 -*-

"""
Buttons for '/start'
"""

from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

def get_cmd_start_buttons() -> ReplyKeyboardMarkup:
	"""
	Generates and returns custom keyboard buttons for the start command.

	:return: Custom keyboard buttons.
	:rtype: ReplyKeyboardMarkup
	"""

	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

	button = KeyboardButton("Выбрать тип расклада", web_app=WebAppInfo(url="https://hse-server.tw1.ru/taro_page_choise_type/"))
	keyboard.add(button)

	return keyboard
