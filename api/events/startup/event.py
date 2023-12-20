"""
Main functions for event startup
"""

from fastapi import FastAPI
import logging

# Импортируем функцию для логирования из файла со вспомогательными функциями

from utils.helper import get_log

# Функция записывающая информацию о начале работы

async def startup_event(api_logger: logging.Logger) -> None:
    """
    Body of event startup.

    :param api_logger: Logger instance for logging startup information.
    :type api_logger: logging.Logger
    """

    api_logger.info(get_log(s = "+", text = f"<-Start->"))

# Функция вызывающаяся при старте и вызывающая событие записывающее информацию о старте с помощью функции startup_event

def setup(app: FastAPI, logger: logging.Logger) -> None:
    """
    Func for setup startup_event.

    :param app: Object of FastAPI.
    :type app: FastAPI
    :param logger: Logger instance for logging startup information.
    :type logger: logging.Logger
    """

     # Инициализируем функцию startup_event внутри основной функции

    async def startup_event_() -> None:
        await startup_event(api_logger = logger)

    # Выполняем событие записи информации о запуске

    app.add_event_handler("startup", startup_event_)