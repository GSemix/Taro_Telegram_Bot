# -*- coding: utf-8 -*-

"""
Functions for table users

:var table: Name of table users
:type table: str
"""

from re import findall

from typing import Dict
from typing import Any
from typing import List
from typing import Optional

from postgresql.model import ClientPostgreSQL
from app.utils.templates.users import table_users

# Задает переменную table со значением названия таблицы пользователей

table = table_users()["table"]

# Получает информацию о пользователе по его идентификатору. Возвращает словарь с данными пользователя или None, если пользователь не найден

async def get_user_by_id(bd: ClientPostgreSQL, id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves user information by their ID from the database.

    :param bd: PostgreSQL database client.
    :type bd: ClientPostgreSQL
    :param id: User ID.
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

# Добавляет нового пользователя в базу данных. Принимает словарь с информацией о пользователе. Возвращает результат операции или None

async def set_user(bd: ClientPostgreSQL, item: Dict[str, Any]) -> Optional[str]:
    """
    Adds a new user to the database.

    :param bd: PostgreSQL database client.
    :type bd: ClientPostgreSQL
    :param item: User information as a dictionary.
    :type item: Dict[str, Any]
    :return: Result of the operation or None.
    :rtype: Optional[str]
    """

    result = await bd.append_item(
        table = table,
        item = item,
        check_twin_colums = ["id"]
    )

    return result

# Проверяет, имеет ли пользователь права доступа. Возвращает True, если пользователь имеет доступ, и False в противном случае

async def isAccess(bd: ClientPostgreSQL, id: int) -> bool:
    """
    Checks if a user has access rights.

    :param bd: PostgreSQL database client.
    :type bd: ClientPostgreSQL
    :param id: User ID.
    :type id: int
    :return: True if the user has access, False otherwise.
    :rtype: bool
    """

    result = await bd.get_items(
        table = table,
        columns = {
            "access"
        },
        by_values = {
            "id": id
        }
    )

    if result:
        result = result[0]["access"]
    else:
        result = False
    
    return result

# Проверяет, является ли пользователь администратором. Возвращает True, если пользователь является администратором, и False в противном случае

async def isAdmin(bd: ClientPostgreSQL, id: int) -> bool:
    """
    Checks if a user is an administrator.

    :param bd: PostgreSQL database client.
    :type bd: ClientPostgreSQL
    :param id: User ID.
    :type id: int
    :return: True if the user is an administrator, False otherwise.
    :rtype: bool
    """

    result = await bd.get_items(
        table = table,
        columns = {
            "admin"
        },
        by_values = {
            "id": id
        }
    )

    if result:
        result = result[0]["admin"]
    else:
        result = False
    
    return result

# Обновляет информацию о пользователе в базе данных. Принимает словарь с обновляемыми значениями и идентификатор пользователя. Возвращает сообщение об ошибке, если обновление не удалось, и None в случае успеха

async def update_user(bd: ClientPostgreSQL, update_values: Dict[str, Any], id: int) -> Optional[str]:
    """
    Updates user information in the database.

    :param bd: PostgreSQL database client.
    :type bd: ClientPostgreSQL
    :param update_values: Dictionary containing the columns to be updated and their new values.
    :type update_values: Dict[str, Any]
    :param id: User ID.
    :type id: int
    :return: Optional error message, None if the update is successful.
    :rtype: Optional[str]
    """

    result = await bd.update_item(
        table = table,
        update_values = update_values,
        by_values = {
            "id": id
        }
    )
    
    return result

#  Обновляет состояние пользователя в базе данных. Принимает новое значение состояния и идентификатор пользователя. Возвращает сообщение об ошибке или None, в случае успеха

async def update_state(bd: ClientPostgreSQL, id: int, value: str) -> Optional[str]:
    """
    Updates the state of a user in the database.

    :param bd: PostgreSQL database client.
    :type bd: ClientPostgreSQL
    :param id: User ID.
    :type id: int
    :param value: New state value.
    :type value: str
    :return: Optional error message, None if the update is successful.
    :rtype: Optional[str]
    """

    result = await bd.update_item(
        table = table,
        update_values = {
            "state": value
        },
        by_values = {
            "id": id
        }
    )
    
    return result

# Получает текущее состояние пользователя из базы данных. Возвращает состояние пользователя или None, если пользователь не найден

async def get_state(bd: ClientPostgreSQL, id: int) -> Optional[str]:
    """
    Retrieves the state of a user from the database.

    :param bd: PostgreSQL database client.
    :type bd: ClientPostgreSQL
    :param id: User ID.
    :type id: int
    :return: User's state, None if the user is not found.
    :rtype: Optional[str]
    """

    result = await bd.get_items(
        table = table,
        columns = [
            "state"
        ],
        by_values = {
            "id": id
        }
    )

    if result:
        result = result[0]["state"]
    else:
        result = None

    return result

# Проверяет, соответствует ли текущее состояние пользователя указанному значению. Возвращает True, если состояние соответствует, и False в противном случае

async def isState(bd: ClientPostgreSQL, id: int, value: str) -> bool:
    """
    Checks if the user's state matches the specified value.

    :param bd: PostgreSQL database client.
    :type bd: ClientPostgreSQL
    :param id: User ID.
    :type id: int
    :param value: State value to check against.
    :type value: str
    :return: True if the user's state matches the specified value, False otherwise.
    :rtype: bool
    """

    result = await bd.get_items(
        table = table,
        columns = [
            "state"
        ],
        by_values = {
            "id": id
        }
    )

    if result:
        result = result[0]["state"]
    else:
        result = None

    return result == value

# Проверяет, содержит ли состояние пользователя указанное значение. Использует регулярное выражение для проверки. Возвращает True, если значение содержится в состоянии, и False в противном случае

async def inState(bd: ClientPostgreSQL, id: int, value: str) -> bool:
    """
    Checks whether the user's state contains the specified value

    :param bd: PostgreSQL database client.
    :type bd: ClientPostgreSQL
    :param id: User ID.
    :type id: int
    :param value: State value to check against.
    :type value: str
    :return: True if the user's state contains the specified value, otherwise False..
    :rtype: bool
    """

    result = await bd.get_items(
        table = table,
        columns = [
            "state"
        ],
        by_values = {
            "id": id
        }
    )

    if result:
        result = result[0]["state"]
    else:
        result = None

    return (len(findall(value, result)) == 1)