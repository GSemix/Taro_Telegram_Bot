"""
Main functions for event startup
"""

from fastapi import FastAPI
import logging

# Импортируем функцию для логирования из файла со вспомогательными функциями

from utils.helper import get_log
from postgresql import ClientPostgreSQL
from app import start_bd

# Функция записывающая информацию о начале работы

async def startup_event(api_logger: logging.Logger, bd: ClientPostgreSQL) -> None:
    """
    Body of event startup.

    :param api_logger: Logger instance for logging startup information.
    :type api_logger: logging.Logger
    """

    await start_bd(bd_var = bd)

    api_logger.info(get_log(s = "+", text = f"<-Start->"))

# Функция вызывающаяся при старте и вызывающая событие записывающее информацию о старте с помощью функции startup_event

def setup(app: FastAPI, logger: logging.Logger, bd: ClientPostgreSQL) -> None:
    """
    Func for setup startup_event.

    :param app: Object of FastAPI.
    :type app: FastAPI
    :param logger: Logger instance for logging startup information.
    :type logger: logging.Logger
    :param bd: An instance of the ClientPotgreSQL class representing the PostgreSQL database.
    :type bd: ClientPostgreSQL  
    """

     # Инициализируем функцию startup_event внутри основной функции

    async def startup_event_() -> None:
        await startup_event(api_logger = logger, bd = bd)

    # Выполняем событие записи информации о запуске

    app.add_event_handler("startup", startup_event_)