"""
Requests table and struct
"""

from typing import Dict
from typing import Any
from typing import List

# Функция возвращает шаблон для запроса в виде словаря

def json_requests() -> Dict[str, Any]:
    """
    Returns a dictionary template for a request.

    :return: Dictionary template for a request.
    :rtype: Dict[str, Any]
    """

    return {
        "id": 0,
        "user_id": 0,
        "cards": []
        "request": "",
        "response": ""
    }

# Функция возвращает название и колонки с типами для таблицы запросов

def table_requests() -> Dict[str, List[str]]:
    """
    Returns a dictionary template for creating a requests table in a database.

    :return: Dictionary template for creating a requests table.
    :rtype: Dict[str, str]
    """

    return {
        "table": "requests",
        "columns": [
            "id BIGINT PRIMARY KEY",
            "user_id BIGINT",
            "cards TEXT[] NOT NULL",
            "request TEXT",
            "response TEXT"
        ]
    }