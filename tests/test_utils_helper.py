"""
Testing utils/helper.py
"""

import unittest

from utils.helper import get_log
from utils.helper import get_log_with_id
from utils.helper import isInt
from utils.helper import isFloat

class TestUtilityFunctions(unittest.TestCase):
    """
    Class for testing helper functions
    """
    def test_get_log(self) -> None:
        """
        Check getting log
        """
        self.assertEqual(get_log("!", "test message"), "[!] test message")
        self.assertEqual(get_log("+", "success"), "[+] success")

    def test_get_log_with_id(self) -> None:
        """
        Check getting log with id
        """
        self.assertEqual(get_log_with_id(1, "!", "user logged in"), "1 : [!] user logged in")
        self.assertEqual(get_log_with_id(2, "+", "user created"), "2 : [+] user created")

    def test_isInt(self) -> None:
        """
        Checking if integer
        """
        self.assertTrue(isInt("123"))
        self.assertFalse(isInt("123.45"))
        self.assertFalse(isInt("123.45qwe"))
        self.assertFalse(isInt("abc"))

    def test_isFloat(self) -> None:
        """
        Checking if float
        """
        self.assertTrue(isFloat("123"))
        self.assertTrue(isFloat("123.45"))
        self.assertFalse(isInt("123.45qwe"))
        self.assertFalse(isFloat("abc"))

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
