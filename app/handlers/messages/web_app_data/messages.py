# -*- coding: utf-8 -*-

"""
Messages for Web App data
"""

from typing import List
from typing import Dict

from aiogram import types
from aiogram.types import Message

from custom_classes import Bot_

async def send_choise_type_taro_message(bot: Bot_, message: Message, type_taro: str) -> None:
	"""
	Sends a message indicating the selected tarot type to the user.

	:param bot: Telegram Bot instance.
	:type bot: Bot\_
	:param message: Message object.
	:type message: Message
	:param type_taro: Selected tarot type.
	:type type_taro: str
	"""

	await bot.send_message(message.from_user.id, text = f"Выбран тип \"{type_taro}\"", parse_mode=types.ParseMode.HTML)
