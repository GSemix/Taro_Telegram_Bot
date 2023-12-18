"""
Testing /utils/file.py
"""

import unittest
import os
import json

from utils.file import get_json_data
from utils.file import get_json_data_with_int_keys
from utils.file import convert_json_data_to_key_int
from utils.file import write_json_data
from utils.file import get_data
from utils.file import set_data

class TestFileFunctions(unittest.TestCase):
	"""
	Class for testing auxiliary functions for files

	:ivar test_json_file: Name of json temp file for testing
	:type test_json_file: str
	:ivar test_text_file: Name of test text temp file for testing
	:type test_text_file: str
	:ivar sample_json_data: Example of json
	:type assample_json_datad: Dict[str, str]
	:ivar sample_text_data: Example of text
	:type sample_text_data: str
	"""
	def setUp(self) -> None:
		"""
		Called at the beginning of each function for testing
		"""
		self.test_json_file = 'test.json'
		self.test_text_file = 'test.txt'
		self.sample_json_data = {"1": "a", "2": "b"}
		self.sample_text_data = "Sample text data"

		with open(self.test_json_file, 'w', encoding='utf8') as f:
			json.dump(self.sample_json_data, f)

		with open(self.test_text_file, 'w', encoding='utf8') as f:
			f.write(self.sample_text_data)

	def tearDown(self) -> None:
		"""
		Clean up after running tests
		"""
		os.remove(self.test_json_file)
		os.remove(self.test_text_file)

	def test_get_json_data(self) -> None:
		"""
		Check json data from temp jeon file
		"""
		data = get_json_data(self.test_json_file)
		self.assertEqual(data, self.sample_json_data)

	def test_get_json_data_with_int_keys(self) -> None:
		"""
		Check getting keys of dict from temp json file
		"""
		data = get_json_data_with_int_keys(self.test_json_file)
		expected_data = {int(k): v for k, v in self.sample_json_data.items()}
		self.assertEqual(data, expected_data)

	def test_convert_json_data_to_key_int(self) -> None:
		"""
		Check convert keys of dict from temp json file
		"""
		converted_data = convert_json_data_to_key_int(self.sample_json_data)
		expected_data = {int(k): v for k, v in self.sample_json_data.items()}
		self.assertEqual(converted_data, expected_data)

	def test_write_json_data(self) -> None:
		"""
		Check writing json data in temp file
		"""
		new_data = {"3": "c", "4": "d"}
		write_json_data(self.test_json_file, new_data)
		with open(self.test_json_file, 'r', encoding='utf8') as f:
			data = json.load(f)
		self.assertEqual(data, new_data)

	def test_get_data(self) -> None:
		"""
		Check getting data from text temp file
		"""
		data = get_data(self.test_text_file)
		self.assertEqual(data, self.sample_text_data)

	def test_set_data(self) -> None:
		"""
		Check writing data to temp text file
		"""
		new_data = "New sample text"
		set_data(self.test_text_file, new_data)
		with open(self.test_text_file, 'r', encoding='utf8') as f:
			data = f.read()
		self.assertEqual(data, new_data)

	def test_get_json_data_file_not_found_error(self) -> None:
		"""
		Check getting json data from temp file if FileNotFoundError
		"""
		with self.assertRaises(FileNotFoundError):
			get_json_data("non_existent_file.json")

	def test_get_json_data_with_int_keys_key_error(self) -> None:
		"""
		Check getting json data from temp file with int keys if ValueError
		"""
		with open('temp_test.json', 'w', encoding='utf8') as f:
			json.dump({"a": "1", "b": "2"}, f)

		with self.assertRaises(ValueError):
			get_json_data_with_int_keys('temp_test.json')

		os.remove('temp_test.json')

	def test_write_json_data_file_not_found_error(self) -> None:
		"""
		Check writing json data to temp file if FileNotFoundError
		"""
		with self.assertRaises(FileNotFoundError):
			write_json_data("/unwritable_path/test.json", {"1": "a"})

	def test_get_data_file_not_found_error(self) -> None:
		"""
		Check getting data from text temp file if FileNotFoundError
		"""
		with self.assertRaises(FileNotFoundError):
			get_data("non_existent_file.txt")

	def test_set_data_file_not_found_error(self) -> None:
		"""
		Check writing data to text temp file if FileNotFoundError
		"""
		with self.assertRaises(FileNotFoundError):
			set_data("/unwritable_path/test.txt", "Sample text")

if __name__ == '__main__':
	unittest.main()
