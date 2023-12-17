# -*- coding: utf-8 -*-

"""
Functions are used to work with files
"""

from json import dump
from json import load

from typing import Dict
from typing import Any

# Возвращает содержимое файла в формате JSON
def get_json_data(file_name: str) -> Dict[str, Any]:
    """Returns the contents of a json file

    :param file_name: Stores the path of the file
    :type file_name: str
    :returns: data
    :rtype: Dict[str, Any]
    """

    with open(file_name, 'r') as file:
        data = load(file)

    return data

# Возвращает содержимое файла в формате JSON с ключами типа int.
def get_json_data_with_int_keys(file_name: str) -> Dict[int, Any]:
    """Returns the contents of a json file with keys type int

    :param file_name: Stores the path of the file
    :type file_name: str
    :returns: data
    :rtype: Dict[int, Any]
    """

    data = get_json_data(file_name)

    return convert_json_data_to_key_int(data)

# Возвращает словарь с ключами типа int
def convert_json_data_to_key_int(data: Dict[str, Any]) -> Dict[int, Any]:
    """Returns the dict with keys type int

    :param data: Dict for writing
    :type data: Dict[str, Any]
    :returns: new
    :rtype: Dict[int, Any]
    """

    new = {}
    for x in data.keys():
        new[int(x)] = data[x]

    return new

# Записывает данные в формате JSON в файл с указанным именем.
def write_json_data(file_name: str, data: Dict[str, Any]) -> None:
    """Returns None. Write the data to a json file named file_name

    :param file_name: Stores the path of the file
    :type file_name: str
    :param data: Dict for writing
    :type data: Dict[str, Any]
    """

    with open(file_name, 'w', encoding='utf8') as file:
        dump(data, file, ensure_ascii=False, indent=4)

# Возвращает содержимое текстового файла в виде строки.
def get_data(file_name: str) -> str:
    """Returns None. Write the data to a file named file_name

    :param file_name: Stores the path of the file
    :type file_name: str
    :returns: data
    :rtype: str
    """

    with open(file_name, 'r') as file:
        data = file.read()

    return data

# Записывает строку в текстовый файл.
def set_data(file_name: str, data: str) -> None:
    """Returns None. Write the data to a file named file_name

    :param file_name: Stores the path of the file
    :type file_name: str
    :param data: String to write
    :type data: str
    """

    with open(file_name, 'w') as file:
        file.write(data)
