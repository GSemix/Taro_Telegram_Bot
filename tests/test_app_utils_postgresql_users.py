# -*- coding: utf-8 -*-

"""
Testing app/utils/postgresql/users.py
"""

import unittest
import asyncio
from unittest.mock import AsyncMock

from app.utils.postgresql.users import get_user_by_id
from app.utils.postgresql.users import set_user
from app.utils.postgresql.users import isAccess
from app.utils.postgresql.users import isAdmin
from app.utils.postgresql.users import update_user
from app.utils.postgresql.users import get_state
from app.utils.postgresql.users import isState
from app.utils.postgresql.users import inState

class TestUserFunctions(unittest.IsolatedAsyncioTestCase):
    """
    Class for testing auxiliary table user's functions

    :ivar mock_db: Async mock PostgreSQL data base
    :type mock_db: AsyncMock
    :ivar user_data: Example user's data
    :type user_data: Dict[str, Any]
    """

    async def asyncSetUp(self) -> None:
        """
        Called at the beginning of each function for testing
        """
        # Настройка моковой базы данных
        self.mock_db = AsyncMock()
        # Настройка примеров пользователей
        self.user_data = {"id": 1, "name": "Test User", "access": True, "admin": True, "state": "active_1337"}

    async def test_get_user_by_id(self) -> None:
        """
        Check find user's row by id
        """
        # Предполагаем, что пользователь найден
        self.mock_db.get_items.return_value = [self.user_data]
        result = await get_user_by_id(self.mock_db, 1)
        self.assertEqual(result, self.user_data)

    async def test_set_user(self) -> None:
        """
        Check try add user's row
        """
        # Тестирование добавления нового пользователя
        self.mock_db.append_item.return_value = None
        result = await set_user(self.mock_db, self.user_data)
        self.assertIsNone(result)

    async def test_isAccess(self) -> None:
        """
        Check user's access
        """
        # Тестирование наличия прав доступа у пользователя
        self.mock_db.get_items.return_value = [self.user_data]
        result = await isAccess(self.mock_db, 1)
        self.assertTrue(result)

    async def test_isAdmin(self) -> None:
        """
        Check user's admin status
        """
        # Тестирование статуса администратора пользователя
        self.mock_db.get_items.return_value = [self.user_data]
        result = await isAdmin(self.mock_db, 1)
        self.assertTrue(result)

    async def test_update_user(self) -> None:
        """
        Check update user's row
        """
        # Тестирование обновления информации пользователя
        self.mock_db.update_item.return_value = None
        result = await update_user(self.mock_db, {"name": "Updated User"}, 1)
        self.assertIsNone(result)

    async def test_get_state(self) -> None:
        """
        Check user's state
        """
        # Тестирование получения состояния пользователя
        self.mock_db.get_items.return_value = [self.user_data]
        result = await get_state(self.mock_db, 1)
        self.assertEqual(result, "active_1337")

    async def test_isState(self) -> None:
        """
        Check user's state compliance
        """
        self.mock_db.get_items.return_value = [self.user_data]
        result = await isState(self.mock_db, 1, "active_1337")
        self.assertTrue(result)

    async def test_inState(self) -> None:
        """
        Check for a certain value in the user state
        """
        self.mock_db.get_items.return_value = [self.user_data]
        result = await inState(self.mock_db, 1, "active_\d+")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
