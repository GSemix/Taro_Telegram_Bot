"""
Main functions for event shutdown
"""

from fastapi import FastAPI
import logging

# Импортируем функцию для логирования из файла со вспомогательными функциями

from utils.helper import get_log

# Функция записывающая информацию о завершении работы 

async def shutdown_event(api_logger: logging.Logger) -> None:
    """
    Body of event shutdown.

    :param api_logger: Logger instance for logging shutdown information.
    :type api_logger: logging.Logger
    """

    api_logger.info(get_log(s = "+", text = f"<-Stop->"))

# Функция вызывающаяся при старте и вызывающая событие записывающее информацию о старте с помощью функции shutdown_event

def setup(app: FastAPI, logger: logging.Logger) -> None:
    """
    Func for setup shutdown_event.

    :param app: Object of FastAPI.
    :type app: FastAPI
    :param logger: Logger instance for logging shutdown information.
    :type logger: logging.Logger
    """

    # Инициализируем функцию shutdown_event внутри основной функции

    async def shutdown_event_() -> None:
        await shutdown_event(api_logger = logger)

    # Выполняем событие записи информации о завершении

    app.add_event_handler("shutdown", shutdown_event_)