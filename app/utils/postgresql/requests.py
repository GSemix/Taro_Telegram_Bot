# -*- coding: utf-8 -*-

"""
Functions for table requests

:var table: Name of table requests
:type table: str
"""

from re import findall

from typing import Dict
from typing import Any
from typing import List
from typing import Optional

from postgresql.model import ClientPostgreSQL
from app.utils.templates.requests import table_requests

# Задает переменную table со значением названия таблицы запросов

table = table_requests()["table"]

# Получает информацию о запросе по его идентификатору. Возвращает словарь с данными запроса или None, если запрос не найден

async def get_request_by_id(bd: ClientPostgreSQL, id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves user information by their ID from the database.

    :param bd: PostgreSQL database client.
    :type bd: ClientPostgreSQL
    :param id: requests ID.
    :type id: int
    :return: User information as a dictionary or None if not found.
    :rtype: Optional[Dict[str, Any]]
    """ 
    
    result = await bd.get_items(
        table = table,
        by_values = {
            "id": id
        }
    )

    if result:
        result = result[0]
    else:
        result = None
    return result

# Добавляет новый запрос в базу данных. Принимает словарь с информацией о запросе. Возвращает результат операции или None

async def set_request(bd: ClientPostgreSQL, item: Dict[str, Any]) -> Optional[int]:
    """
    Adds a new request to the database.

    :param bd: PostgreSQL database client.
    :type bd: ClientPostgreSQL
    :param item: Request information as a dictionary.
    :type item: Dict[str, Any]
    :return: Id of appended item or None.
    :rtype: Optional[int]
    """

    result = await bd.append_item(
        table = table,
        item = item,
        returning_columns = ["id"]
    )

    if result:
        return result[0]["id"]

    return None