# -*- coding: utf-8 -*-

"""
Testing Logger
"""

import unittest
import logging
import os
from pydantic import SecretStr
import tempfile

from app.core.logger import get_logger

class TestLogger(unittest.TestCase):
    """
    Class for testing logger

    :ivar temp_dir: Temp random dir
    :ivar temp_dir: tempfile.TemporaryDirectory
    :ivar level: Minimum level for creating a log
    :type level: SecretStr
    :ivar fmt: Log message format
    :type fmt: SecretStr
    :ivar datefmt: Time format
    :type datefmt: SecretStr
    :ivar name: Name of the log file
    :type name: SecretStr
    :ivar path: Path of the log files
    :type path: SecretStr
    :ivar max_bytes: Maximum file size in bytes
    :type max_bytes: SecretStr
    :ivar backup_count: Maximum number of files
    :type backup_count: SecretStr
    :ivar logger: Object for logging
    :type logger: logging.Logger
    """

    def setUp(self) -> None:
        """
        Called at the beginning of each function for testing
        """

        # Предполагаем, что это примеры входных данных для функции get_logger
        self.temp_dir = tempfile.TemporaryDirectory()
        self.level = SecretStr("DEBUG")
        self.fmt = SecretStr("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.datefmt = SecretStr("%Y-%m-%d %H:%M:%S")
        self.name = SecretStr("test_logger")
        self.path = SecretStr(self.temp_dir.name + "/")
        self.max_bytes = SecretStr(str(1024 * 1024 * 10))  # 10MB
        self.backup_count = SecretStr("5")

        self.logger = get_logger(self.level, self.fmt, self.datefmt, self.name, self.path, self.max_bytes, self.backup_count)

    def tearDown(self) -> None:
        """
        Clean up after running tests
        """

        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def test_logger_creation(self) -> None:
        """
        Check creation logger
        """
        self.assertIsInstance(self.logger, logging.Logger)

    def test_logger_level(self) -> None:
        """
        Check logger's level
        """
        self.assertEqual(self.logger.level, logging.getLevelName(self.level.get_secret_value()))

    def test_invalid_logging_level(self) -> None:
        """
        Check invalid logger's level
        """
        invalid_level = SecretStr("NOTALEVEL")
        with self.assertRaises(ValueError):
            get_logger(invalid_level, self.fmt, self.datefmt, self.name, self.path, self.max_bytes, self.backup_count)

    def test_logger_formatter(self) -> None:
        """
        Check logger's ftm
        """
        for handler in self.logger.handlers:
            self.assertIsInstance(handler.formatter, logging.Formatter)
            self.assertEqual(handler.formatter._fmt, self.fmt.get_secret_value())

    def test_logger_handlers(self) -> None:
        """
        Check logger's handlers
        """
        self.assertTrue(len(self.logger.handlers) > 0)
        for handler in self.logger.handlers:
            self.assertIsInstance(handler, logging.handlers.RotatingFileHandler)

    def test_invalid_file_path(self) -> None:
        """
        Check invalid logger's path
        """
        invalid_path = SecretStr("/invalid/path/")
        with self.assertRaises(FileNotFoundError):
            get_logger(self.level, self.fmt, self.datefmt, self.name, invalid_path, self.max_bytes, self.backup_count)

    def test_logger_name(self) -> None:
        """
        Check logger's name
        """
        self.assertEqual(self.logger.name, self.name.get_secret_value())

    def test_logger_max_bytes_and_backup_count(self) -> None:
        """
        Check logger's max_bytes and backup_count
        """
        handler = self.logger.handlers[0]  # Assuming the RotatingFileHandler is the first handler
        self.assertEqual(handler.maxBytes, int(self.max_bytes.get_secret_value()))
        self.assertEqual(handler.backupCount, int(self.backup_count.get_secret_value()))

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
