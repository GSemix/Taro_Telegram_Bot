# -*- coding: utf-8 -*-

"""
Handler for text
"""

from typing import Optional

from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
import openai
from aiohttp import ClientSession
from aiohttp import TCPConnector
from aiohttp_socks import ProxyConnector
from json import dumps
import random
import requests
from asyncio.exceptions import CancelledError

from . import analyze_cards
from . import analyze_prompt
from . import check_quest
from .messages import send_taro_message
from .messages import send_cards_message
from .messages import send_bad_request_message
from .messages import send_show_message

from app.utils.postgresql.users import isAccess
from app.utils.postgresql.users import isState
from app.utils.postgresql.users import isAdmin
from app.utils.postgresql.users import inState
from app.utils.postgresql.users import get_state
from app.utils.postgresql.users import update_state

from utils.helper import get_log_with_id
from utils.file import get_json_data
from utils.file import write_json_data
from app.utils.handlers.shared_messages import send_block_message
from app.utils.handlers.shared_messages import send_error_message

async def handle_text(message: types.Message, dp: Dispatcher, bot_name: Optional[str] = None):
	"""
	This function processes incoming text messages, performs various actions based on the content, and sends appropriate responses.

	:param message: The incoming text message.
	:type message: types.Message
	:param dp: The Dispatcher instance for handling updates.
	:type dp: Dispatcher
	:param bot_name: Optional parameter representing the bot's name.
	:type bot_name: Optional[str]

	:raises CancelledError: If the asynchronous task is canceled.
	:raises Exception: If any unexpected error occurs during message handling.
	"""

	@dp.async_task
	async def handler():
		from app import logger
		from app import bd
		from app import bot
		from app import proxy_cfg
		from app import openai_cfg

		id = message.from_user.id
		text = message.text
		action = None
		action_message_id = message.message_id

		proxy_cfg = proxy_cfg.dict()
		openai_cfg = openai_cfg.dict()

		for x in proxy_cfg.keys():
			proxy_cfg[x] = proxy_cfg[x].get_secret_value()

		proxy_url = f"{proxy_cfg['socks']}://{proxy_cfg['user']}:{proxy_cfg['password']}@{proxy_cfg['host']}:{proxy_cfg['port']}"
		api_key = openai_cfg["api_token"].get_secret_value()
		model_gpt = openai_cfg["model"].get_secret_value()

		if await isAccess(bd = bd, id = id):
			logger.info(get_log_with_id(id = id, s = '=', text = f"Text message: {text}"))
			try:
				await send_show_message(bot = bot, message = message, reply_to_message_id = message.message_id)

				count_cards = 5

				if await inState(bd = bd, id = id, value = "cards_\d+"):
					state = await get_state(bd = bd, id = id)
					count_cards = int(state.split("_")[-1])

				action = types.ChatActions.TYPING
				cards_dict = get_json_data(file_name = "data/cards.json")
				cards = list(cards_dict.keys())
				random_cards_without_flipped = {}

				while len(random_cards_without_flipped) < count_cards:
					card = random.choice(cards)
					if card not in random_cards_without_flipped.keys():
						random_cards_without_flipped[card] = cards_dict[card]

				random_cards = {}

				for key, value in random_cards_without_flipped.items():
					if random.choice([True, False]):
						image_path = value["image"].split("/")
						image_path[-1] = "flip_" + image_path[-1]
						image_path = "/".join(image_path)

						value["image"] = image_path
						random_cards[key + " (Перевернутая карта)"] = value
					else:
						random_cards[key] = value

				await bot.send_chat_action(chat_id = message.from_user.id, action = action, action_message_id = action_message_id)

				check = None
				try:
					connector = ProxyConnector.from_url(proxy_url)
					async with ClientSession(connector=connector) as session:
						openai.aiosession.set(session)
						check = await openai.ChatCompletion.acreate(
							model=model_gpt,
							messages=[
								{"role": "user", "content": check_quest + "\n" + text}
							],
							request_timeout=600,
							api_key=api_key
						)
						check = check.choices[0].message.content
				except openai.error.Timeout as e:
					logger.warning(get_log_with_id(id = id, s = '-', text = f"Слишком долго сервер не отвечает -> {e}"))
					raise Exception(f"{model_gpt} check_quest ({e})")
				except openai.error.InvalidRequestError as e:
					logger.warning(get_log_with_id(id = id, s = '-', text = f"Слишком много токенов -> {e}"))
					raise Exception(f"{model_gpt}check_quest ({e})")
				except openai.error.RateLimitError as e:
					logger.warning(get_log_with_id(id = id, s = '-', text = f"Слишком частые сообщения -> {e}"))
					raise Exception(f"{model_gpt} check_quest ({e})")
				except openai.error.APIError as e:
					logger.warning(get_log_with_id(id = id, s = '-', text = f"Ошибка сервера -> {e}"))
					raise Exception(f"{model_gpt} check_quest ({e})")
				except Exception as e:
					logger.warning(get_log_with_id(id = id, s = '-', text = f"Неизвестная ошибка -> {e}"))
					raise Exception(f"{model_gpt} check_quest ({e})")

				if "CORRECT" in check:
					await send_cards_message(bot = bot, message = message, cards = random_cards, reply_to_message_id = message.message_id)

					chat = None
					try:
						connector = ProxyConnector.from_url(proxy_url)
						async with ClientSession(connector=connector) as session:
							openai.aiosession.set(session)
							chat = await openai.ChatCompletion.acreate(
								model=model_gpt,
								messages=[
									{"role": "system", "content": analyze_cards},
									{"role": "user", "content": "Расклад:" + "\n" + "\n".join(key for key in random_cards) + "Запрос:" + "\n" + text}
								],
								request_timeout=600,
								api_key=api_key
							)
							chat = chat.choices[0].message.content
					except openai.error.Timeout as e:
						logger.warning(get_log_with_id(id = id, s = '-', text = f"Слишком долго сервер не отвечает -> {e}"))
						raise Exception(f"{model_gpt} analyze_cards ({e})")
					except openai.error.InvalidRequestError as e:
						logger.warning(get_log_with_id(id = id, s = '-', text = f"Слишком много токенов -> {e}"))
						raise Exception(f"{model_gpt} analyze_cards ({e})")
					except openai.error.RateLimitError as e:
						logger.warning(get_log_with_id(id = id, s = '-', text = f"Слишком частые сообщения -> {e}"))
						raise Exception(f"{model_gpt} analyze_cards ({e})")
					except openai.error.APIError as e:
						logger.warning(get_log_with_id(id = id, s = '-', text = f"Ошибка сервера -> {e}"))
						raise Exception(f"{model_gpt} analyze_cards ({e})")
					except Exception as e:
						logger.warning(get_log_with_id(id = id, s = '-', text = f"Неизвестная ошибка -> {e}"))
						raise Exception(f"{model_gpt} analyze_cards ({e})")

					prompt = None
					try:
						connector = ProxyConnector.from_url(proxy_url)
						async with ClientSession(connector=connector) as session:
							openai.aiosession.set(session)
							prompt = await openai.ChatCompletion.acreate(
								model=model_gpt,
								messages=[
									{"role": "user", "content": analyze_prompt + "\n" + chat}
								],
								request_timeout=600,
								api_key=api_key
							)
							prompt = prompt.choices[0].message.content
					except openai.error.Timeout as e:
						logger.warning(get_log_with_id(id = id, s = '-', text = f"Слишком долго сервер не отвечает -> {e}"))
						raise Exception(f"{model_gpt} ({e})")
					except openai.error.InvalidRequestError as e:
						logger.warning(get_log_with_id(id = id, s = '-', text = f"Слишком много токенов -> {e}"))
						raise Exception(f"{model_gpt} ({e})")
					except openai.error.RateLimitError as e:
						logger.warning(get_log_with_id(id = id, s = '-', text = f"Слишком частые сообщения -> {e}"))
						raise Exception(f"{model_gpt} ({e})")
					except openai.error.APIError as e:
						logger.warning(get_log_with_id(id = id, s = '-', text = f"Ошибка сервера -> {e}"))
						raise Exception(f"{model_gpt} ({e})")
					except Exception as e:
						logger.warning(get_log_with_id(id = id, s = '-', text = f"Неизвестная ошибка -> {e}"))
						raise Exception(f"{model_gpt} prompt ({e})")

					response = None
					try:
						connector = ProxyConnector.from_url(proxy_url)
						async with ClientSession(connector=connector) as session:
							openai.aiosession.set(session)
							response = await openai.Image.acreate(
								prompt=prompt,
								n=1,
								size="256x256",
								api_key=api_key
							)
							url = response["data"][0]["url"]
							response = requests.get(url)
					except Exception as e:
						raise Exception(f"dall-e ({e})")

					if response.status_code == 200:
						await send_taro_message(bot = bot, message = message, text = chat, photo = response.content, action = action, action_message_id = action_message_id, reply_to_message_id = message.message_id)
					else:
						raise Exception(f"dall-e (bad get request -> {response.status_code})")
				else:
					await send_bad_request_message(bot = bot, message = message, text = check, action = action, action_message_id = action_message_id, reply_to_message_id = message.message_id)
			except CancelledError:
				pass
			except Exception as e:
				await send_error_message(bot = bot, message = message, e = e, action = action, action_message_id = action_message_id)
				logger.error(get_log_with_id(id = id, s = '-', text = e))
		else:
			await send_block_message(bot = bot, message = message)

	await handler()

def setup(dp: Dispatcher, bot_name: Optional[str] = None):
	"""
	This function registers a message handler for handling text messages using the provided Dispatcher instance.

	:param dp: The Dispatcher instance for handling updates.
	:type dp: Dispatcher
	:param bot_name: Optional parameter representing the bot's name.
	:type bot_name: Optional[str]
	"""

	dp.register_message_handler(lambda message: handle_text(message, dp, bot_name))