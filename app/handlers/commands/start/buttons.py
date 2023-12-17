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

	button = KeyboardButton("Выбрать тип расклада", web_app=WebAppInfo(url="https://d04c-2001-ac8-59-202-97dd-9040-8716-18.ngrok-free.app"))
	keyboard.add(button)

	return keyboard