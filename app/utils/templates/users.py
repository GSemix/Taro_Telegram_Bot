"""
Users table and struct
"""

from typing import Dict
from typing import Any
from typing import List

# Функция возвращает шаблон для пользователя в виде словаря

def json_user() -> Dict[str, Any]:
    """
    Returns a dictionary template for a user.

    :return: Dictionary template for a user.
    :rtype: Dict[str, Any]
    """

    return {
        "id": 0,
        "username": "username",
        "access": True,
        "admin": False,
        "state": "main"
    }

# Функция возвращает название и колонки с типами для таблицы пользователей

def table_users() -> Dict[str, List[str]]:
    """
    Returns a dictionary template for creating a users table in a database.

    :return: Dictionary template for creating a users table.
    :rtype: Dict[str, str]
    """

    return {
        "table": "users",
        "columns": [
            "id BIGINT PRIMARY KEY",
            "username TEXT",
            "access BOOLEAN NOT NULL",
            "admin BOOLEAN NOT NULL",
            "state TEXT"
        ]
    }