# -*- coding: utf-8 -*-

"""
Staffing and launching Telegram-bot
"""

import asyncio
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook

from . import dp
from . import on_startup
from . import on_shutdown
from . import telegram_cfg

from app.handlers.commands.start import setup as handler_command_start_setup
from app.handlers.commands.help import setup as handler_command_help_setup
from app.handlers.messages.text import setup as handler_messages_text_setup
from app.handlers.messages.web_app_data import setup as handler_messages_web_app_data 

handler_command_start_setup(dp)
handler_command_help_setup(dp)
handler_messages_text_setup(dp)
handler_messages_web_app_data(dp)

start_webhook(
	dispatcher=dp,
	webhook_path=telegram_cfg.webhook_path.get_secret_value(),
	on_startup=on_startup,
	on_shutdown=on_shutdown,
	skip_updates=True,
	host=telegram_cfg.webapp_host.get_secret_value(),
	port=int(telegram_cfg.webapp_port.get_secret_value()),
) # Comment this for polling !!!

#executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True) # Uncomment this line for polling !!!







