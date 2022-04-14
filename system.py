"""! @brief Методы для работы с ОС."""
##
# @file system.py
#
# @brief Все связанное с взаимодействием с файлами системы.
#
# @section description_system Описание
# Предоставление методов для работы с файловой системой ОС
#
# @section libraries_system Модули
# - os стандартная библиотека
#   - Получение возможности для взаимодействия с ОС
# - requests
#   - Получение содержимого с html документа.
#
# @section notes_system Заметки
#
# @section list_of_changes_system Список изменений
#   - Файл создан Савинов В.В. 14/04/2022
#   - Добавлена doxygen документация Нестеренко А.И. 14/04/2022 
#
# @section author_system Авторы
# - Савинов В.В.
# - Нестеренко А.И.
#
# Copyright (c) 2022 ИРИБ.  All rights reserved.


import os
import requests


def make_directory(filename: str):
    """! mkdir
    
    Этот метод используется для проверки директории на наличие,
    если таковой нет, то будет создана

    @param filename Название директории  
    """
    if os.path.exists(filename):
        return
    os.mkdir(filename)


def save_file(path: str, name: str, url: str, extension: str) -> None:
    """! Save shedule file
    
    Этот метод используется для сохранения расписания в директорию института

    @param path Название директории внутри папки General
    @param name Название файла
    @param url  Ссылка на файл
    @param extension    Расширение файла 
    """
    make_directory(f'General/{path}')
    f = open(f'General/{path}/{name}.{extension}', "wb")
    file = requests.get(url)
    f.write(file.content)
    f.close()
