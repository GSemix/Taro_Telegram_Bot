"""
Testing ClientPotgreSQL
"""

from typing import Dict
from typing import Any
from typing import List
from json import dumps

from . import ClientPotgreSQL
from . import default_postgresql_cfg
from . import default_postgres_logger_cfg
from .core.logger import get_logger

def user():
	return {
		'id': 0,
		'username': 'username',
		'list_bool': [True, True],
		'json_list': [dumps({"a": "b"}), dumps({"b": "c"})],
		'access': True,
		'admin': False,
		'state': 'main'
    }

def table_test_users(): 
	return {
		"table": "test_users",
		"columns": [
			"id BIGINT PRIMARY KEY",
			"username TEXT",
			"list_bool BOOLEAN[]",
			"json_list JSON[]",
			"access BOOLEAN NOT NULL",
			"admin BOOLEAN NOT NULL",
			"state TEXT"
		]
	}

async def main():
	logger = get_logger(**default_postgres_logger_cfg.dict())
	bd = ClientPotgreSQL(default_postgresql_cfg.dict(), logger)
	await bd.create_pool()

	try:
		await bd.check_table(**table_test_users())
		print(await bd.append_item(
			table = "test_users",
			item = user(),
    		check_twin_colums = [
    			"id"
    		])
		)
		print(await bd.get_items(
			table = "test_users",
			columns = ["id", "username"],
			by_values = {
				"id": 0
			})
		)
		print(await bd.update_item(table = "test_users", update_values = {"admin": False, "list_bool": [True, False], "json_list": [dumps({"a": "b"}), dumps({"b": "c"})], "access": True}, by_values = {"id": 0, "username": "username"}))
		print(await bd.delete_item(table = "test_users", by_values = {"id": 0, "username": "username"}))
	except Exception as e:
		print(e)

	await bd.close_pool()

import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(main())