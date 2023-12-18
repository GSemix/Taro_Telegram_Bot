"""
Module for tests
"""

import unittest

def run_tests() -> None:
	"""
	Func for starting all tests in /tests
	"""

	loader = unittest.TestLoader()
	suite = loader.discover('.', pattern='test_*.py')
	runner = unittest.TextTestRunner()
	runner.run(suite)