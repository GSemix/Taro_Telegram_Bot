# -*- coding: utf-8 -*-

"""
Messages for '/help'
"""

from aiogram.types import Message

from custom_classes import Bot_

async def send_cmd_help_message(bot: Bot_, message: Message) -> None:
	"""
	Sends a help message in response to a command.

	:param bot: The bot instance.
	:type bot: Bot\_
	:param message: The original message.
	:type message: Message
	"""

	await bot.send_message(message.from_user.id, text = "Help")