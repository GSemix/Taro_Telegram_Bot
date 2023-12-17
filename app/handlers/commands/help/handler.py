# -*- coding: utf-8 -*-

"""
Handler for '/help'
"""

from typing import Optional

from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from asyncio.exceptions import CancelledError

from .messages import send_cmd_help_message
from app.utils.postgresql.users import isAccess
from app.utils.handlers.shared_messages import send_error_message
from app.utils.handlers.shared_messages import send_block_message
from utils.helper import get_log_with_id

async def cmd_help(message: Message, dp: Dispatcher, bot_name: Optional[str] = None):
	"""
	This function is a coroutine that processes the '/help' command. It checks if the user has access,
	logs the command press, and sends the help message if the user has access.

	:param message: The incoming message that triggered the command.
	:type message: Message
	:param dp: The Dispatcher instance for handling updates.
	:type dp: Dispatcher
	:param bot_name: Optional parameter representing the bot's name.
	:type bot_name: Optional[str]

	:raises CancelledError: If the coroutine is cancelled.
	:raises Exception: If an unexpected error occurs during command processing.
	"""

	@dp.async_task
	async def handler():
		from app import logger
		from app import bd
		from app import bot

		id = message.from_user.id
		if await isAccess(bd = bd, id = id):
			logger.info(get_log_with_id(id = id, s = '=', text = "Pressed '/help'"))
			try:
				await send_cmd_help_message(bot = bot, message = message)
			except CancelledError:
				pass
			except Exception as e:
				await send_error_message(bot = bot, message = message, e = e)
				logger.error(get_log_with_id(id = id, s = '-', text = e))
		else:
			await send_block_message(bot = bot, message = callback_query)

	await handler()

def setup(dp: Dispatcher, bot_name: Optional[str] = None):
	"""
	This function registers a message handler for the '/help' command using the provided Dispatcher instance.

	:param dp: The Dispatcher instance for handling updates.
	:type dp: Dispatcher
	:param bot_name: Optional parameter representing the bot's name.
	:type bot_name: Optional[str]

	:raises ValueError: If the provided Dispatcher instance is not valid.
	"""

	dp.register_message_handler(lambda message: cmd_help(message, dp, bot_name), commands=['help'])