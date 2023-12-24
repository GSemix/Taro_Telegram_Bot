# -*- coding: utf-8 -*-

"""
Messages for text
"""

from typing import List
from typing import Dict

from aiogram import types
from aiogram.types import Message

from custom_classes import Bot_
from .buttons import get_show_buttons

async def send_taro_message(bot: Bot_, message: Message, text: str, photo: bytes, action: str, action_message_id: int, reply_to_message_id: int) -> None:
	"""
	Sends a tarot message with a photo and explanation.

	:param bot: The bot instance.
	:type bot: Bot\_
	:param message: The original message.
	:type message: Message
	:param text: The explanation text.
	:type text: str
	:param photo: The photo bytes.
	:type photo: bytes
	:param action: The action type.
	:type action: str
	:param action_message_id: The ID of the action message.
	:type action_message_id: int
	:param reply_to_message_id: The ID of the message to reply to.
	:type reply_to_message_id: int
	"""

	await bot.send_photo(message.from_user.id, photo = photo, parse_mode=types.ParseMode.HTML, reply_to_message_id = reply_to_message_id)
	await bot.send_message(message.from_user.id, text = "<b>Объяснение:</b>" + "\n" + text, parse_mode=types.ParseMode.HTML, action = action, action_message_id = action_message_id, reply_to_message_id = reply_to_message_id)

async def send_cards_message(bot: Bot_, message: Message, cards: Dict[str, Dict[str, str]], reply_to_message_id: int) -> None:
	"""
	Sends a message with a media group containing tarot cards.

	:param bot: The bot instance.
	:type bot: Bot\_
	:param message: The original message.
	:type message: Message
	:param cards: Dictionary containing tarot card data.
	:type cards: Dict[str, Dict[str, str]]
	:param reply_to_message_id: The ID of the message to reply to.
	:type reply_to_message_id: int
	"""

	first = True
	media = types.MediaGroup()

	for value in cards.values():
		if first:
			media.attach_photo(types.InputFile(value["image"]), "\n".join([f"{index + 1}. {item}" for index, item in enumerate(key for key in cards)]))
			first = False
		else:
			media.attach_photo(types.InputFile(value["image"]))

	await bot.send_media_group(message.from_user.id, media = media, reply_to_message_id = reply_to_message_id)

async def send_bad_request_message(bot: Bot_, message: Message, text: str, action: str, action_message_id: int, reply_to_message_id: int) -> None:
	"""
	Sends a message indicating a bad request.

	:param bot: The bot instance.
	:type bot: Bot\_
	:param message: The original message.
	:type message: Message
	:param text: The text of the bad request message.
	:type text: str
	:param action: The action to be performed.
	:type action: str
	:param action_message_id: The ID of the message to associate with the action.
	:type action_message_id: int
	:param reply_to_message_id: The ID of the message to reply to.
	:type reply_to_message_id: int
	"""

	await bot.send_message(message.from_user.id, text = text, action = action, action_message_id = action_message_id, reply_to_message_id = reply_to_message_id)

async def send_show_message(bot: Bot_, message: Message, reply_to_message_id: int) -> None:
	"""
	Sends a show cards message.

	:param bot: The bot instance.
	:type bot: Bot\_
	:param message: The original message.
	:type message: Message
	:param reply_to_message_id: The ID of the message to reply to.
	:type reply_to_message_id: int
	"""

	await bot.send_message(message.from_user.id, text = "Тестовый расклад", reply_markup = get_show_buttons(), reply_to_message_id = reply_to_message_id)




