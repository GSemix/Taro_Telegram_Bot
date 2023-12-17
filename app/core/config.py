# -*- coding: utf-8 -*-

"""
Telegram, PostgreSQL, Proxy, OpenAI and their Loggers Configuration Classes
"""

from pydantic import BaseSettings, SecretStr

# Конфигурация Telegram бота
class TelegramConfig(BaseSettings):
    """Represents the Telegram bot configuration.

    :cvar token: The Telegram bot token
    :type token: SecretStr
    :cvar webhook_host: The host for Telegram webhook
    :type webhook_host: SecretStr
    :cvar webhook_path: The path for Telegram webhook
    :type webhook_path: SecretStr
    :cvar webhook_url: The full URL for Telegram webhook
    :type webhook_url: SecretStr
    :cvar webapp_host: The host for the web application
    :type webapp_host: SecretStr
    :cvar webapp_port: The port for the web application
    :type webapp_port: SecretStr
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

        env_prefix = "TELEGRAM_"
        env_file = '.env'
        env_file_encoding = 'utf-8'

    token: SecretStr
    webhook_host: SecretStr
    webhook_path: SecretStr
    webhook_url: SecretStr
    webapp_host: SecretStr
    webapp_port: SecretStr

# Конфигурация логирования для Telegram бота
class TelegramLoggingConfig(BaseSettings):
    """Represents the Telegram bot logging configuration.
    
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

        env_prefix = "TELEGRAM_LOGGING_"
        env_file = '.env'
        env_file_encoding = 'utf-8'

    level: SecretStr
    fmt: SecretStr
    datefmt: SecretStr
    name: SecretStr
    path: SecretStr
    max_bytes: SecretStr
    backup_count: SecretStr

# Конфигурация для PostgreSQL
class PostgreSQLConfig(BaseSettings):
    """Represents the PostgreSQL configuration.

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
        env_file = '.env'
        env_file_encoding = 'utf-8'

    host: SecretStr
    port: SecretStr
    user: SecretStr
    password: SecretStr
    database: SecretStr
    min_size: SecretStr
    max_size: SecretStr
    max_queries: SecretStr

# Конфигурация логирования для PostgreSQL
class PostgreSQLLoggingConfig(BaseSettings):
    """Represents the PostgreSQL logging configuration.
    
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
        env_file = '.env'
        env_file_encoding = 'utf-8'

    level: SecretStr
    fmt: SecretStr
    datefmt: SecretStr
    name: SecretStr
    path: SecretStr
    max_bytes: SecretStr
    backup_count: SecretStr

# Конфигурация прокси
class ProxyConfig(BaseSettings):
    """Represents the Proxy States configuration.

    :cvar socks: The SOCKS proxy URL
    :type socks: SecretStr
    :cvar host: The hostname or IP address of the proxy server
    :type host: SecretStr
    :cvar port: The port number for the proxy server
    :type port: SecretStr
    :cvar user: The username for authentication with the proxy server
    :type user: SecretStr
    :cvar password: The password for authentication with the proxy server
    :type password: SecretStr
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

        env_prefix = "PROXY_"
        env_file = '.env'
        env_file_encoding = 'utf-8'

    socks: SecretStr
    host: SecretStr
    port: SecretStr
    user: SecretStr
    password: SecretStr

# Конфигурация для OpenAI
class OpenAIConfig(BaseSettings):
    """Represents the OpenAI States configuration.

    :cvar api_token: A string of characters used for authentication and authorization when interacting with the API
    :type api_token: SecretStr
    :cvar model: GPT model
    :type model: SecretStr
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

        env_prefix = "OPENAI_"
        env_file = '.env'
        env_file_encoding = 'utf-8'

    api_token: SecretStr
    model: SecretStr






