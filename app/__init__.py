# -*- coding: utf-8 -*-

"""
Module for Telegram-bot

:var postgresql_cfg: An instance of PostgreSQLConfig used for configuring PostgreSQL settings
:type postgresql_cfg: PostgreSQLConfig
:var postgres_logger_cfg: An instance of PostgreSQLLoggingConfig used for configuring PostgreSQL logging settings
:type postgres_logger_cfg: PostgreSQLLoggingConfig
:var postgres_logger: A logger for PostgreSQL interactions, configured using postgres_logger_cfg settings
:type postgres_logger: logging.Logger
:var bd: An instance of ClientPotgreSQL with PostgreSQLConfig settings and PostgreSQL logger
:type bd: ClientPotgreSQL
:var telegram_cfg: An instance of TelegramConfig used for configuring Telegram settings
:type telegram_cfg: TelegramConfig
:var telegram_logger_cfg: An instance of TelegramLoggingConfig used for configuring Telegram logging settings
:type telegram_logger_cfg: TelegramLoggingConfig
:var logger: A logger for Telegram interactions, configured using telegram_logger_cfg settings
:type logger: logging.Logger
:var bot: An instance of Bot\_ representing the Telegram bot, initialized with a Telegram token and logger
:type bot: Bot\_
:var dp: A Dispatcher instance for handling incoming Telegram updates, associated with the bot
:type dp: Dispatcher
:var proxy_cfg: Settings from ProxyConfig
:type proxy_cfg: ProxyConfig
:var openai_cfg: Settings from OpenAIConfig
:type openai_cfg: OpenAIConfig
"""

from custom_classes import Bot_
from aiogram import types
from aiogram.dispatcher import Dispatcher

from .core.config import TelegramLoggingConfig
from .core.config import TelegramConfig
from .core.config import PostgreSQLLoggingConfig
from .core.config import PostgreSQLConfig
from .core.config import ProxyConfig
from .core.config import OpenAIConfig
from .core.logger import get_logger
from postgresql import ClientPostgreSQL
from utils.helper import get_log
from .utils.templates.users import table_users
from .utils.templates.requests import table_requests

async def set_default_commands(dp: Dispatcher):
    """
    Sets default commands for the bot (blue button 'Menu')

    :param dp: The Dispatcher object from aiogram associated with the bot
    :type dp: Dispatcher
    """

    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Старт'),
            types.BotCommand('help', 'Помощь')
        ]
    )

async def start_bd(bd_var: ClientPostgreSQL):
    """
    Asynchronously starts the PostgreSQL database connection and performs initial setup

    :param bd_var: An instance of the ClientPotgreSQL class representing the PostgreSQL database.
    :type bd_var: ClientPostgreSQL    
    """

    await bd_var.create_pool()
    await bd_var.check_table(**table_users())
    await bd_var.check_table(**table_requests())

async def on_startup(dp: Dispatcher):
    """
    Asynchronous function called on application startup

    :param dp: The Dispatcher object from aiogram associated with the bot
    :type dp: Dispatcher
    """

    await start_bd(bd_var = bd)
    await bot.set_webhook(telegram_cfg.webhook_url.get_secret_value()) # Comment this line for polling !!!
    await set_default_commands(dp)
    logger.info(get_log('=', "<-START->"))

async def on_shutdown(dp: Dispatcher):
    """
    Asynchronous function called on application shutdown

    :param dp: The Dispatcher object from aiogram associated with the bot
    :type dp: Dispatcher
    """

    await bd.close_pool()
    await dp.bot.close_tasks()
    await bot.delete_webhook() # Comment this line for polling !!!
    logger.info(get_log('=', "<-STOP->"))

postgresql_cfg = PostgreSQLConfig()
postgres_logger_cfg = PostgreSQLLoggingConfig()
postgres_logger = get_logger(**postgres_logger_cfg.dict())
bd = ClientPostgreSQL(postgresql_cfg.dict(), postgres_logger)

telegram_cfg = TelegramConfig()
telegram_logger_cfg = TelegramLoggingConfig()
logger = get_logger(**telegram_logger_cfg.dict())
bot = Bot_(token = telegram_cfg.token.get_secret_value(), logger = logger) # Объект бота
dp = Dispatcher(bot) # Диспетчер

proxy_cfg = ProxyConfig()
openai_cfg = OpenAIConfig()





