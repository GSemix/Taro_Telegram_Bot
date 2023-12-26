"""
Buttons for text
"""

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

def get_show_buttons(request_id: int) -> InlineKeyboardMarkup:
	"""
	Generates and returns custom keyboard buttons for show cards.

	:return: Custom keyboard buttons.
	:rtype: ReplyKeyboardMarkup
	"""

	keyboard = InlineKeyboardMarkup(resize_keyboard=True)

	button = InlineKeyboardButton("👀 Смотреть", web_app=WebAppInfo(url=f"https://hse-server.tw1.ru/taro_page_show/?id={request_id}"))
	keyboard.add(button)

	return keyboard