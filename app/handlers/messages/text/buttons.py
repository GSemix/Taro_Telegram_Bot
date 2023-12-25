"""
Buttons for text
"""

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

def get_show_buttons() -> InlineKeyboardMarkup:
	"""
	Generates and returns custom keyboard buttons for show cards.

	:return: Custom keyboard buttons.
	:rtype: ReplyKeyboardMarkup
	"""

	keyboard = InlineKeyboardMarkup(resize_keyboard=True)

	button = InlineKeyboardButton("Выбрать тип расклада", web_app=WebAppInfo(url="https://hse-server.tw1.ru/taro_page_show/?id=1"))
	keyboard.add(button)

	return keyboard