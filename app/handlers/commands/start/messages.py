# -*- coding: utf-8 -*-

"""
Messages for '/start'
"""

from aiogram import types
from aiogram.types import Message

from custom_classes import Bot_

from .buttons import get_cmd_start_buttons

async def send_cmd_start_message(bot: Bot_, message: Message) -> None:
	"""
	Sends a start message in response to a command.

	:param bot: The bot instance.
	:type bot: Bot\_
	:param message: The original message.
	:type message: Message
	"""

	await bot.send_message(message.from_user.id, text = f"""Привет, {message.from_user.username}! 👋
		🔮 Добро пожаловать в мир таро! Я – Эсмеральда, ваш надёжный гид в путешествии по картам судьбы.
		<b>Задайте свой вопрос прямо в чат</b>, и я открою перед вами тайны и подскажу пути. Таро – это зеркало души и ключ к пониманию тайн.
		Пусть ваше путешествие будет полно открытий и прозрений! ✨
		""", reply_markup=get_cmd_start_buttons(), parse_mode=types.ParseMode.HTML)