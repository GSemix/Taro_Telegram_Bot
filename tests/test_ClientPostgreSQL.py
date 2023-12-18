# -*- coding: utf-8 -*-

"""
Testing ClientPostgreSQL class.

:var table: Name of test table
:type table: str
:var columns: Columns of test table
:type columns: List[str]
"""

from typing import Any
from typing import List
from typing import Dict

import unittest
import asyncpg
from pydantic import SecretStr

from postgresql import ClientPostgreSQL

def test_table() -> Dict[str, List[str]]:
    """
    Returns a dictionary template for creating a test table in a database.

    :return: Dictionary template for creating a test table.
    :rtype: Dict[str, List[str]]
    """
    return {
        "table": "test_table",
        "columns": [
            "id serial PRIMARY KEY",
            "data TEXT",
            "list TEXT[]"
        ]
    }

table = test_table()["table"]
columns = test_table()["columns"]

class TestClientPostgreSQL(unittest.IsolatedAsyncioTestCase):
    """
    Class for testing methods of ClientPostgreSQL

    :ivar client: Object for DB communication
    :type client: ClientPostgreSQL
    """
    async def asyncSetUp(self) -> None:
        """
        Called at the beginning of each function for testing
        """

        postgres_cfg = {
            "host": SecretStr("127.0.0.1"),
            "port": SecretStr("5432"),
            "user": SecretStr("myuser"),
            "password": SecretStr("mypass"),
            "database": SecretStr("mybase"),
            "min_size": SecretStr("3"),
            "max_size": SecretStr("10"),
            "max_queries": SecretStr("500")
        }
        self.client = ClientPostgreSQL(params=postgres_cfg)
        await self.client.create_pool()  # assuming this creates a pool for the test database
        result = await self.client.check_table(**test_table())
        self.assertIsNotNone(result)

    async def test_execute(self) -> None:
        """
        Check execute line
        """
        result = await self.client.execute(query = "SELECT 1;")
        self.assertIsInstance(result, str)
        self.assertEqual(result, "SELECT 1")

    async def test_execute_error(self) -> None:
        """
        Check execute line with invalide query
        """
        #with self.assertRaises(asyncpg.PostgresError):
        result = await self.client.execute(query = "some_invalid_input")
        self.assertIsNone(result)

    async def test_fetch(self) -> None:
        """
        Check feth line
        """
        query = f"SELECT * FROM {table} LIMIT 1;"
        result = await self.client.fetch(query)
        self.assertIsInstance(result, list)

    async def test_fetch_error(self) -> None:
        """
        Check feth line with invalide query
        """
        query = "some_invalid_input"
        result = await self.client.fetch(query)
        self.assertIsNone(result)

    async def test_fetchrow(self) -> None:
        """
        Check fetchrow line
        """
        query = f"SELECT * FROM {table};"
        result = await self.client.fetchrow(query)
        self.assertIsInstance(result, dict)  # Проверяем, что результат - это словарь

    async def test_fetchrow_error(self) -> None:
        """
        Check fetchrow line with invalide query
        """
        query = "some_invalid_input"
        result = await self.client.fetchrow(query)
        self.assertIsNone(result)

    async def test_table_exists(self) -> None:
        """
        Check test table exist
        """
        result = await self.client.table_exists(table)
        self.assertIsInstance(result, list)  # Проверяем, что результат - это список

    async def test_create_table(self) -> None:
        """
        Check test table creation
        """
        result = await self.client.create_table(table = table, columns = ",\n".join(columns))
        self.assertIsInstance(result, str)

    async def test_update_item(self) -> None:
        """
        Check item update
        """
        update_values = {"data": "new_data"}
        by_values = {"id": -1}
        result = await self.client.update_item(table, update_values, by_values)
        self.assertIsInstance(result, str)

    async def test_update_item_error(self) -> None:
        """
        Check item update with invalide data
        """
        update_values = {"bad_column": "bad_data"}
        by_values = {"id": -1}
        result = await self.client.update_item(table, update_values, by_values)
        self.assertIsNone(result)

    async def test_append_item(self) -> None:
        """
        Check append item
        """
        item = {
            "data": "Test Item",
            "list": ["qwe"]
        }
        result = await self.client.append_item(table, item)
        self.assertIsNotNone(result)

    async def test_append_item_error(self) -> None:
        """
        Check append item with invalide data
        """
        item = {
            "bad_data": "bad item"
        }
        result = await self.client.append_item(table, item)
        self.assertIsNone(result)

    async def test_delete_item(self) -> None:
        """
        Check delete item
        """
        by_values = {"id": 1}
        result = await self.client.delete_item(table, by_values)
        self.assertIsInstance(result, str)

    async def test_delete_item_error(self) -> None:
        """
        Check delete item with invalide data
        """
        by_values = {"bad_column": -1}
        result = await self.client.delete_item(table, by_values)
        self.assertIsNone(result)

    async def test_get_items(self) -> None:
        """
        Check getting item
        """
        columns = ["data"]
        by_values = {"id": -1}
        result = await self.client.get_items(table, columns, by_values)
        self.assertIsInstance(result, list)  # Проверяем, что результат - это список

    async def test_get_items_error(self) -> None:
        """
        Check getting item with invalide data
        """
        columns = ["data"]
        by_values = {"bad_id": -1}
        result = await self.client.get_items(table, columns, by_values)
        self.assertIsNone(result)

    async def test_update_item_with_append(self) -> None:
        """
        Check update item with append
        """
        update_values = {"list": ["new_value"]}
        by_values = {"id": -1}
        result = await self.client.update_item_with_append(table, update_values, by_values)
        self.assertIsInstance(result, str)

    async def test_update_item_with_append_error(self) -> None:
        """
        Check update item with append if data is invalide
        """
        update_values = {"list": ["new_value"]}
        by_values = {"bad_id": -1}
        result = await self.client.update_item_with_append(table, update_values, by_values)
        self.assertIsNone(result)

    async def asyncTearDown(self) -> None:
        """
        Clean up code that runs after each test. Close the database connection.
        """
        await self.client.execute(query = f"DROP TABLE IF EXISTS {table};")
        await self.client.close_pool()

if __name__ == '__main__':
    unittest.main()
 




