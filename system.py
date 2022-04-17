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
#   - Добавлены методы Савинов В.В. 15/04/2022:
#       - get_path_schedule_files
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


def get_path_schedule_files() -> list:
    """! Get full path to all shedule files

    Получение полного путя до каждого расписания
    
    @return Список путей до каждого Excel файла
    """
    initial_path = f'{os.getcwd()}\\General\\'
    os.chdir(initial_path)
    final_paths = []
    for root, dirs, files in os.walk(".", topdown=False):
        for file in files:
            n = initial_path + os.path.join(root, file)[2:]
            final_paths.append(n)
    return final_paths


def main():
    """! Function to test and debug code

    Эта функция используется для отладки написанного кода
    """
    print(get_path_schedule_files())

if __name__ == '__main__':
    main()
