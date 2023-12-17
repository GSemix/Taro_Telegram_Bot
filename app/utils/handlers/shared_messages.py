# -*- coding: utf-8 -*-

"""
Shared messages
"""

# Импортируем виды данных

from typing import Any
from typing import List
from typing import Optional

from aiogram import types
from aiogram.types import Message
from aiogram.types import base

# Импортируем кастомный класс бота

from custom_classes import Bot_

# Функция получает на вход данные о сообщении которое вызвало ошибку, данные об ошибке, и действие в ходе которго была получена ошибка и присылает в ответ сообщение об ошибке

async def send_error_message(bot: Bot_, message: Message, e: Exception, action: Optional[base.String] = None, action_message_id: Optional[int] = None) -> None:
    """
    This function formats an error message with the exception details and sends it to the user.

    :param bot: The Bot\_ instance for sending the message.
    :type bot: Bot\_
    :param message: The original incoming message.
    :type message: Message
    :param e: The exception that occurred.
    :type e: Exception
    :param action: Name of action
    :type action: Optional[base.String]
    :param action_message_id: Action message's id
    :type action_message_id: Optional[int]
    """

    # Через message.from_user.id получает информацию о чате в который нужно отправить сообщение, отправляет сообщение об ошибке интерпритируя его как HTML и записывает в логи информацию из action и action_id

    await bot.send_message(message.from_user.id, text = f"<b>Ошибка:</b> {e}", parse_mode = types.ParseMode.HTML, action = action, action_message_id = action_message_id)

# Функция выдающая пользователю сообщение об отсутствии прав доступа

async def send_block_message(bot: Bot_, message: Message) -> None:
    """
    This function sends a message to the user indicating that they do not have the necessary access rights.

    :param bot: The Bot\_ instance for sending the message.
    :type bot: Bot\_
    :param message: The original incoming message.
    :type message: Message
    """

    # Через message.from_user.id получает информацию о чате в который нужно отправить сообщение, отправляет сообщение об отсутствии прав доступа интерпритируя его как HTML

    await bot.send_message(message.from_user.id, text = f"<b>😨 У вас нет прав доступа, обратитесь к администраторам</b>", parse_mode = types.ParseMode.HTML)



