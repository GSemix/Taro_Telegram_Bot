# -*- coding: utf-8 -*-

"""
Handler for '/start'
"""

from typing import Optional

from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from asyncio.exceptions import CancelledError

from utils.helper import get_log_with_id
from utils.helper import isInt
from app.utils.postgresql.users import get_user_by_id
from app.utils.postgresql.users import set_user
from app.utils.postgresql.users import isAccess
from app.utils.postgresql.users import isAdmin
from app.utils.postgresql.users import update_user
from app.utils.postgresql.users import isState
from app.utils.postgresql.users import update_state
from app.utils.templates.users import json_user
from app.utils.handlers.shared_messages import send_error_message
from app.utils.handlers.shared_messages import send_block_message
from .messages import send_cmd_start_message

async def cmd_start(message: Message, dp: Dispatcher, bot_name: Optional[str] = None):
	"""
	This function is a coroutine that processes the '/start' command. It checks if the user has access,
	updates user information, and sends an appropriate response message.

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
		username = message.from_user.username

		logger.info(get_log_with_id(id = id, s = '=', text = "Pressed '/start'"))

		try:
			user = await get_user_by_id(bd = bd, id = id)

			if not user:
				user = json_user()
				user["id"] = id
				user["username"] = username

				await set_user(bd = bd, item = user)
				logger.info(get_log_with_id(id = id, s = '+', text = "Append new user"))
			else:
				if await isAccess(bd = bd, id = id):
					await update_user(
						bd = bd,
						update_values = {
							"username": username
						},
						id = id
					)
					await update_state(bd = bd, id = id, value = "main")
					logger.info(get_log_with_id(id = id, s = '+', text = "Info about user updated"))

			if await isAccess(bd = bd, id = id):
				await send_cmd_start_message(bot = bot, message = message)
			else:
				await send_block_message(bot = bot, message = message)
				logger.warning(get_log_with_id(id = id, s = '?', text = "Detected user without ACCESS"))
		except CancelledError:
			pass
		except Exception as e:
			await send_error_message(bot = bot, message = message, e = e)
			logger.error(get_log_with_id(id = id, s = '-', text = f"Error: {e}"))

	await handler()

def setup(dp: Dispatcher, bot_name: Optional[str] = None):
	"""
	This function registers a message handler for the '/start' command using the provided Dispatcher instance.

	:param dp: The Dispatcher instance for handling updates.
	:type dp: Dispatcher
	:param bot_name: Optional parameter representing the bot's name.
	:type bot_name: Optional[str]

	:raises ValueError: If the provided Dispatcher instance is not valid.
	"""

	dp.register_message_handler(lambda message: cmd_start(message, dp, bot_name), commands=['start'])