# -*- coding: utf-8 -*-

"""
Script and function for flipping photos
"""
# Импортируем класс Image для работы с изображениями карт Таро

from PIL import Image

# Из file импортируем функции для считывания и записи информации из json файла

from file import get_json_data
from file import write_json_data

# Функция переворачивает изображения из input_path и сохраняет его в output_path

def flip_upside_down(input_path: str, output_path: str) -> None:
    """Flips photo with input_path 180 degrees and saves it to output_path

    :param input_path: Path of Image
    :type input_path: str
    :param output_path: Path to save modified image
    :type output_path: str
    """

    # ОткрываеТ изображение из input_path
    original_image = Image.open(input_path)

    # Переворачивает изображение на 180 градусов
    flipped_image = original_image.rotate(180)

    # Сохраняет перевернутое изображение в файл с output_path
    flipped_image.save(output_path)

# Этот код обрабатывается только при запуске самого файла

if __name__=="__main__":

    # Проходится по каждой карте из списка cards.json, из input_path получает output_path и с помощью функции flip_upside_down переворачивает на 180 градусов каждую карту и сохраняет их в отдельные файлы по адресу output_path

    for key, value in get_json_data("../data/cards.json").items():
        input_image_path = "../" + value["image"]
        output_image_path = value["image"].split("/")
        output_image_path[-1] = "flip_" + output_image_path[-1]
        output_image_path = "../" + "/".join(output_image_path)

        # Переворачиваем изображение вверх ногами с помощью функции flip_upside_down
        flip_upside_down(input_image_path, output_image_path)
        print(output_image_path)