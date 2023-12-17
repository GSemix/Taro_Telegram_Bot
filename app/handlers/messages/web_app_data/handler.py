# -*- coding: utf-8 -*-

"""
Handler for Web App data
"""

from typing import Optional

from json import loads
from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from asyncio.exceptions import CancelledError

from utils.helper import get_log_with_id
from utils.file import get_json_data
from app.utils.postgresql.users import isAccess
from app.utils.postgresql.users import isState
from app.utils.postgresql.users import update_state
from app.utils.handlers.shared_messages import send_error_message
from app.utils.handlers.shared_messages import send_block_message
from .messages import send_choise_type_taro_message

async def web_app_data(webAppMes: Message, dp: Dispatcher, bot_name: Optional[str] = None):
    """
    This function processes incoming data from the Web App, performs various actions based on the content, and sends appropriate responses.

    :param webAppMes: The incoming web app message.
    :type webAppMes: Message
    :param dp: The Dispatcher instance for handling updates.
    :type dp: Dispatcher
    :param bot_name: Optional parameter representing the bot's name.
    :type bot_name: Optional[str]

    :raises CancelledError: If the asynchronous task is canceled.
    :raises Exception: If any unexpected error occurs during data handling.
    """

    @dp.async_task
    async def handler():
        from app import logger
        from app import bd
        from app import bot

        id = int(webAppMes.from_user.id)
        data = loads(webAppMes.web_app_data.data)
        print(data)

        logger.info(get_log_with_id(id = id, s = '=', text = f"web_app_data: {data}"))

        if await isAccess(bd = bd, id = id):
            try:
                if data['type'] == 'choise_type_taro':
                    type_taro = data["name"]
                    await update_state(bd = bd, id = id, value = type_taro)

                    json_data = get_json_data(file_name = "data/types_taro.json")

                    await send_choise_type_taro_message(bot = bot, message = webAppMes, type_taro = json_data[type_taro])
                else:
                    await send_block_message(bot = bot, message = webAppMes)
                    logger.warning(get_log_with_id(id = id, s = '?', text = "Detected user without ACCESS"))
            except CancelledError as e:
                print(e)
            except Exception as e:
                await send_error_message(bot = bot, message = webAppMes, e = e)
                logger.error(get_log_with_id(id = id, s = '-', text = f"Error: {e}"))

    await handler()

def setup(dp: Dispatcher, bot_name: Optional[str] = None):
    """
    This function registers a message handler for handling Web App data messages using the provided Dispatcher instance.

    :param dp: The Dispatcher instance for handling updates.
    :type dp: Dispatcher
    :param bot_name: Optional parameter representing the bot's name.
    :type bot_name: Optional[str]
    """

    dp.register_message_handler(lambda message: web_app_data(message, dp, bot_name), content_types="web_app_data")




