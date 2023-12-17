# -*- coding: utf-8 -*-

"""
Database and Logger Configuration Classes
"""

from pydantic import BaseSettings, SecretStr

class DefaultPostgreSQLConfig(BaseSettings):
    """Represents the Default PostgreSQL configuration

    :cvar host: DB address
    :type host: SecretStr
    :cvar port: DB port
    :type port: SecretStr
    :cvar user: DB user
    :type user: SecretStr
    :cvar password: DB password
    :type password: SecretStr
    :cvar database: DB name
    :type database: SecretStr
    :cvar min_size: Minimum number of connections in the pool
    :type min_size: SecretStr
    :cvar max_size: Maximum number of connections in the pool
    :type max_size: SecretStr
    :cvar max_queries: The maximum number of requests that can be made on a single connection before it is returned to the pool
    :type max_queries: SecretStr
    """

    class Config:
        """
        Represents parameters for reading configuration

        :cvar env_prefix: Parameter prefix in the file
        :type env_prefix: str
        :cvar env_file: Configuration file name
        :type env_file: str
        :cvar env_file_encoding: Configuration file encoding
        :type env_file_encoding: str
        """

        env_prefix = "POSTGRESQL_"
        env_file = '.test_postgresql_env'
        env_file_encoding = 'utf-8'

    host: SecretStr
    port: SecretStr
    user: SecretStr
    password: SecretStr
    database: SecretStr
    min_size: SecretStr
    max_size: SecretStr
    max_queries: SecretStr

class DeafultPostgreSQLLoggingConfig(BaseSettings):
    """Represents the Default PostgreSQL logger configuration
    
    :cvar level: Minimum level for creating a log
    :type level: SecretStr
    :cvar fmt: Log message format
    :type fmt: SecretStr
    :cvar datefmt: Time format
    :type datefmt: SecretStr
    :cvar name: Name of the log file
    :type name: SecretStr
    :cvar path: Path of the log files
    :type path: SecretStr
    :cvar max_bytes: Maximum file size in bytes
    :type max_bytes: SecretStr
    :cvar backup_count: Maximum number of files
    :type backup_count: SecretStr
    """

    class Config:
        """
        Represents parameters for reading configuration

        :cvar env_prefix: Parameter prefix in the file
        :type env_prefix: str
        :cvar env_file: Configuration file name
        :type env_file: str
        :cvar env_file_encoding: Configuration file encoding
        :type env_file_encoding: str
        """

        env_prefix = "POSTGRESQL_LOGGING_"
        env_file = '.test_postgresql_env'
        env_file_encoding = 'utf-8'

    level: SecretStr
    fmt: SecretStr
    datefmt: SecretStr
    name: SecretStr
    path: SecretStr
    max_bytes: SecretStr
    backup_count: SecretStr