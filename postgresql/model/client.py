# -*- coding: utf-8 -*-

"""
Class for interacting with PostgreSQL.

This class provides methods for executing queries, fetching results, checking table existence,
creating tables, appending items, updating items, deleting items, and managing a PostgreSQL connection pool.
"""

import asyncpg
import asyncio
import logging

from typing import Dict
from typing import Any
from typing import List
from typing import Optional

from utils.helper import get_log
from utils.helper import isInt

class ClientPostgreSQL(object):
    """
    PostgreSQL client for database interactions.

    :ivar pool: PostgreSQL connection pool.
    :type pool: asyncpg.Pool
    :ivar params: Dictionary containing PostgreSQL connection parameters.
    :type params: Dict[str, Any]
    :ivar logger: Logger for recording events.
    :type logger: Optional[logging.Logger]
    """

    class Error(Exception):
        """
        Custom exception class for handling errors in the PostgreSQL client.

        :ivar message: message of error
        :type message: str
        """

        def __init__(self, message: str):
            """
            Initialization Error object.

            :param message: message of error
            :type message: str
            """

            super().__init__(message)
            self.message = message

    def __init__(self, params: Dict[str, Any], logger: Optional[logging.Logger] = None) -> None:
        """
        Initialization Error object.

        :param params: params for db connection
        :type params: Dict[str, Any]
        :param logger: object for logging with default value None
        :type logger: Optional[logging.Logger]
        """

        self.params = params

        for x in self.params.keys():
            try:
                if x in ['min_size', 'max_size', 'max_queries']:
                    self.params[x] = int(self.params[x].get_secret_value())
                else:
                    self.params[x] = self.params[x].get_secret_value()
            except AttributeError:
                pass

        self.pool = None
        self.logger = logger

    def __setattr__(self, key: Any, value: Any) -> None:
        """
        Override the default attribute setting behavior.

        :param key: Attribute key.
        :type key: Any
        :param value: Attribute value.
        :type value: Any
        """

        self.__dict__[key] = value

    async def execute(self, query: str, args: List[Any] = []) -> Optional[str]:
        """
        Executes a SQL query with optional parameters.

        :param query: The SQL query to execute.
        :param args: List of parameters to substitute into the query.
        :return: The result of the query, if any.
        :rtype: Optional[str]
        
        :raises asyncpg.PostgresError: If there is an error during the PostgreSQL execution.
        """

        result = None
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.execute(query, *args)
        except asyncpg.PostgresError as e:
            self.logger.error(get_log('-', e)) if self.logger else None
        self.logger.debug(get_log('+', f"<query>: {query}, <args>: {args}, <result>: {result}")) if self.logger else None

        return result

    async def fetch(self, query: str, args: List[Any] = []) -> Optional[List[Dict[Any, Any]]]:
        """
        Fetch results for a query.

        :param query: PostgreSQL query.
        :type query: str
        :param args: List of arguments for the query with default value [].
        :type args: List[Any]
        :return: List of dictionaries representing the query results.
        :rtype: Optional[List[Dict[Any, Any]]]

        :raises Error: If there is an error fetching results.
        """

        results = None
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    results = await connection.fetch(query, *args)
                    if results:
                        results = [dict(result) for result in results]
        except asyncpg.PostgresError as e:
            self.logger.error(get_log('-', e)) if self.logger else None
        self.logger.debug(get_log('+', f"<query>: {query}, <args>: {args}, <result>: {results}")) if self.logger else None

        return results

    async def fetchrow(self, query: str, args: List[Any] = []) -> Optional[Dict[Any, Any]]:
        """
        Execute a PostgreSQL query and fetch a single row as a dictionary.

        :param query: The PostgreSQL query to execute.
        :type query: str
        :param args: A list of arguments to replace placeholders in the query.
        :type args: List[Any]
        :return: A dictionary representing the fetched row, or None if no rows are returned.
        :rtype: Optional[Dict[Any, Any]]

        :raises asyncpg.PostgresError: If an error occurs while executing the query.
        """

        result = None
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow(query, *args)
                    if result:
                        result = dict(result)
                    else:
                        result = {}
        except asyncpg.PostgresError as e:
            self.logger.error(get_log('-', e)) if self.logger else None
        self.logger.debug(get_log('+', f"<query>: {query}, <args>: {args}, <result>: {result}")) if self.logger else None

        return result

    async def table_exists(self, table: str) -> Optional[List[Dict[Any, Any]]]:
        """
        Check if a table exists in the database.

        :param table: Name of the table to check.
        :type table: str
        :return: List of dictionaries representing the query results.
        :rtype: Optional[List[Dict[Any, Any]]]
        """

        result = None
        database = self.params["database"]
        query = f"SELECT * FROM information_schema.tables WHERE table_name = '{table}' AND table_catalog = '{database}';"
        result = await self.fetch(query = query)
        if result:
            self.logger.info(get_log('+', f"Table '{table}' was detected")) if self.logger else None
        return result

    async def create_table(self, table: str, columns: str) -> Optional[str]:
        """
        Create a table in the database with the specified name and columns.

        :param table: Name of the table to be created.
        :type table: str
        :param columns: Definition of columns in the table.
        :type columns: str
        :return: A string indicating the success or failure of the table creation.
                 Returns None if the table was created successfully; otherwise, an error message.
        :rtype: Optional[str]
        """

        result = None
        query = f"CREATE TABLE IF NOT EXISTS {table}(\n{columns});"
        result = await self.execute(query = query)
        if result:
            self.logger.info(get_log('+', f"Table '{table}' was created")) if self.logger else None
        else:
            self.logger.info(get_log('-', f"Error! Table '{table}' wasn't created")) if self.logger else None
        return result

    async def check_table(self, table: str, columns: List[str]) -> Optional[Any]:
        """
        Check if a table exists; if not, create it.

        :param table: Table name.
        :type table: str
        :param columns: Columns and their data types for the table.
        :type columns: List[str]
        :return: Result of the check or creation.
        :rtype: Optional[Any]
        """

        result = await self.table_exists(table = table)
        if not result:
            result = await self.create_table(table = table, columns = ",\n".join(columns))
        return result

    async def append_item(self, table: str, item: Dict[str, Any], check_twin_colums: List[str] = [], returning_columns: List[str] = []) -> Optional[str]:
        """
        Append an item to the specified table.

        :param table: Table name.
        :type table: str
        :param item: Dictionary representing the item to be appended.
        :type item: Dict[str, Any]
        :param check_twin_colums: List of columns to check for twin items.
        :type check_twin_colums: List[str]
        :param returning_columns: List of columns to return after appending.
        :type returning_columns: List[str]
        :return: Result of the item append operation.
        :rtype: Optional[str]

        :raises Error: If there is an error during the execution of the method.
        """

        results = None
        try:
            if item:
                by_values = {}
                if check_twin_colums:
                    for column in check_twin_colums:
                        if column not in item.keys():
                            raise self.Error(f"Can't check column '{column}' without value!")
                        else:
                            by_values[column] = item[column]
                if not check_twin_colums or not await self.get_items(table=table, columns=["id"], by_values=by_values):
                    values_query = []
                    args = []
                    variables_query = []
                    returning_query = []
                    for key, value in item.items():
                        args.append(value)
                        values_query.append(f"${len(args)}")
                        variables_query.append(key)

                    for column in returning_columns:
                        returning_query.append(column)
                    returning_query = " RETURNING " + ", ".join(returning_query) if returning_query else ""
                    variables_query = ", ".join(variables_query)
                    values_query = f"VALUES({', '.join(values_query)})"
                    query = f"INSERT INTO {table} ({variables_query}) {values_query}{returning_query};"
                    results = await self.fetch(query = query, args = args)
                    if results:
                        self.logger.info(get_log('+', f"Append item in {table}: {item}")) if self.logger else None
                        if results != []:
                            results = [dict(result) for result in results]
                else:
                    self.logger.info(get_log('?', f"Impossible to append item in {table}: {item} will be Twin by columns {check_twin_colums}!")) if self.logger else None
            else:
                self.logger.info(get_log('?', f"Impossible to append empty item in {table}!")) if self.logger else None
        except self.Error as e:
            self.logger.warning(get_log('-', e)) if self.logger else None
        return results

    async def get_items(self, table: str, columns: List[str] = [], by_values: Dict[str, Any] = {}) -> Optional[List[Dict[str, Any]]]:
        """
        Get items from a table based on specified conditions.

        :param table: Name of the table to query.
        :type table: str
        :param columns: List of columns to retrieve with default value [].
        :type columns: List[str]
        :param by_values: Dictionary of column-value pairs to filter results with default value {}.
        :type by_values: Dict[str, Any]
        :return: List of dictionaries representing the query results.
        :rtype: Optional[List[Dict[str, Any]]]

        :raises Error: If there is an error during the database operation.
        """

        results = None
        try:
            selected_columns = '*'
            if columns:
                selected_columns = ", ".join(columns)
            args = []
            where_query = []
            if by_values:
                for key, value in by_values.items():
                    args.append(value)
                    where_query.append(f"{key}=${len(args)}")
                where_query = " WHERE " + " AND ".join(where_query)
            else:
                where_query = ""
            query = f"SELECT {selected_columns} FROM {table}{where_query}"
            results = await self.fetch(query = query, args = args)
        except self.Error as e:
            self.logger.warning(get_log('-', e)) if self.logger else None
        return results

    async def update_item_with_append(self, table: str, update_values: Dict[str, Any], by_values: Dict[str, Any]) -> Optional[str]:
        """
        Update an item in a table with additional append operation.

        :param table: Name of the table to update.
        :type table: str
        :param update_values: Dictionary representing the values to update.
        :type update_values: Dict[str, Any]
        :param by_values: Dictionary representing the conditions for the update.
        :type by_values: Dict[str, Any]
        :return: Result of the update operation.
        :rtype: Optional[str]

        :raises Error: If there is an error during the database operation.
        """

        result = None
        try:
            if not update_values:
                raise self.Error(f"Can't update item without values!")
            args = []
            set_query = []
            where_query = []
            for key, value in update_values.items():
                args.append(value)
                if isinstance(value, list):
                    set_query.append(f"{key} = array_cat({key}, ${len(args)})")
                else:
                    set_query.append(f"{key} = ${len(args)}")
            set_query = "SET " + ", ".join(set_query)
            if by_values:
                for key, value in by_values.items():
                    args.append(value)
                    where_query.append(f"{key} = ${len(args)}")
                where_query = " WHERE " + " AND ".join(where_query)
            else:
                    where_query = ""
            query = f"UPDATE {table} {set_query}{where_query};"
            result = await self.execute(query = query, args = args)
            if result:
                self.logger.info(get_log('+', f"Update values: {update_values} in table '{table}' where {by_values}")) if self.logger else None
        except self.Error as e:
            self.logger.warning(get_log('-', e)) if self.logger else None
        return result

    async def update_item(self, table: str, update_values: Dict[str, Any], by_values: Dict[str, Any]) -> Optional[str]:
        """
        Update an item in a table.

        :param table: Name of the table to update.
        :type table: str
        :param update_values: Dictionary representing the values to update.
        :type update_values: Dict[str, Any]
        :param by_values: Dictionary representing the conditions for the update.
        :type by_values: Dict[str, Any]
        :return: Result of the update operation.
        :rtype: Optional[str]

        :raises Error: If there is an error during the database operation.
        """
        result = None
        try:
            if not update_values:
                raise self.Error(f"Can't update item without values!")
            args = []
            set_query = []
            where_query = []
            for key, value in update_values.items():
                args.append(value)
                set_query.append(f"{key} = ${len(args)}")
            set_query = "SET " + ", ".join(set_query)
            if by_values:
                for key, value in by_values.items():
                    args.append(value)
                    where_query.append(f"{key} = ${len(args)}")
                where_query = " WHERE " + " AND ".join(where_query)
            else:
                    where_query = ""
            query = f"UPDATE {table} {set_query}{where_query};"
            result = await self.execute(query = query, args = args)
            if result:
                self.logger.info(get_log('+', f"Update values: {update_values} in table '{table}' where {by_values}")) if self.logger else None
        except self.Error as e:
            self.logger.warning(get_log('-', e)) if self.logger else None
        return result

    async def delete_item(self, table: str, by_values: Dict[str, Any]) -> Optional[str]:
        """
        Delete items from a table.

        :param table: Name of the table to delete from.
        :type table: str
        :param by_values: Dictionary representing the conditions for deletion.
        :type by_values: Dict[str, Any]
        :return: Result of the delete operation.
        :rtype: Optional[str]

        :raises Error: If there is an error during the database operation.
        """

        result = None
        try:
            args = []
            where_query = []
            if by_values:
                for key, value in by_values.items():
                    args.append(value)
                    where_query.append(f"{key}=${len(args)}")
                where_query = "WHERE " + " AND ".join(where_query)
            else:
                where_query = ""
            query = f"DELETE FROM {table} {where_query};"
            result = await self.execute(query = query, args = args)
            if result:
                self.logger.info(get_log('+', f"Delete items in table '{table}' where {by_values}")) if self.logger else None
        except self.Error as e:
            self.logger.warning(get_log('-', e)) if self.logger else None
        return result

    async def create_pool(self) -> None:
        """
        Create a PostgreSQL connection pool.
        """

        self.pool = await asyncpg.create_pool(**self.params)
        self.logger.info(get_log('+', f"PostgeSQL pool was created")) if self.logger else None

    async def close_pool(self) -> None:
        """
        Close the PostgreSQL connection pool.
        """

        await self.pool.close()
        self.logger.info(get_log('+', f"PostgeSQL pool was closed")) if self.logger else None









