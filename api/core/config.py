# -*- coding: utf-8 -*-

"""
API and Logger Configuration Classes
"""

from pydantic import BaseSettings, SecretStr

class ApiConfig(BaseSettings):
    """Represents the API configuration.

    :cvar host: API's Address
    :type host: SecretStr
    :cvar port: API's port
    :type port: SecretStr
    :cvar workers: Number of workers that will be created to process incoming requests
    :type workers: SecretStr
    :cvar app: module_name\:instance_name
    :type app: SecretStr
    :cvar allow_origins: Allowed Query Sources
    :type allow_origins: SecretStr
    :cvar allow_methods: Allowed Methods
    :type allow_methods: SecretStr
    :cvar allow_headers: Allowed headers
    :type allow_headers: SecretStr
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

        env_prefix = "API_"
        env_file = '.api_env'
        env_file_encoding = 'utf-8'

    host: SecretStr
    port: SecretStr
    workers: SecretStr
    app: SecretStr
    allow_origins: SecretStr
    allow_methods: SecretStr
    allow_headers: SecretStr

class ApiLoggingConfig(BaseSettings):
    """Represents the API logging configuration.
    
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

        env_prefix = "API_LOGGING_"
        env_file = '.api_env'
        env_file_encoding = 'utf-8'

    level: SecretStr
    fmt: SecretStr
    datefmt: SecretStr
    name: SecretStr
    path: SecretStr
    max_bytes: SecretStr
    backup_count: SecretStr



