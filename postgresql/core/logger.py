# -*- coding: utf-8 -*-

"""
Functions for configuring and creating loggers

Logging levels (min -> max):
debug -> info -> warning -> error -> critical
"""

import logging
import logging.handlers
from pydantic import SecretStr

def get_logger(level: SecretStr, fmt: SecretStr, datefmt: SecretStr, name: SecretStr, path: SecretStr, max_bytes: SecretStr, backup_count: SecretStr) -> logging.Logger:
    """Returns сonfigured logger object by parameters

    :param level: Minimum level for creating a log
    :type level: SecretStr
    :param fmt: Log message format
    :type fmt: SecretStr
    :param datefmt: Time format
    :type datefmt: SecretStr
    :param name: Name of the log file
    :type name: SecretStr
    :param path: Path of the log files
    :type path: SecretStr
    :param max_bytes: Maximum file size in bytes
    :type max_bytes: SecretStr
    :param backup_count: Maximum number of files
    :type backup_count: SecretStr
    :returns: logger
    :rtype: logging.Logger
    """

    logger = logging.getLogger(name.get_secret_value())
    logger.setLevel(level.get_secret_value())
    formatter = logging.Formatter(fmt=fmt.get_secret_value(), datefmt=datefmt.get_secret_value())
    handler = logging.handlers.RotatingFileHandler(
        f'{path.get_secret_value()}{name.get_secret_value()}.out', maxBytes=int(max_bytes.get_secret_value()), backupCount=int(backup_count.get_secret_value())) # 1024 * 1024 * 10
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger