"""! @brief Утилиты, которые могут понадобиться при работе"""
##
# @file utils.py
#
# @brief Методы, которые невозможно нормально группировать
#
# @section description_utils Описание
# Сборная солянка из разных методов
#
# @section libraries_utils Модули
# - transliterate
#   - Транслитерация слов на английский язык
# - datetime
#   - Получение текущего времени системы
#
# @section notes_utils Заметки
#
# @section list_of_changes_utils Список изменений
#   - Файл создан Савинов В.В. 14/04/2022
#   - Добавлена doxygen документация Нестеренко А.И. 14/04/2022 
#
# @section author_utils Авторы
# - Савинов В.В.
# - Нестеренко А.И.
#
# Copyright (c) 2022 ИРИБ.  All rights reserved.


import transliterate
from datetime import datetime


def transliteration_to_en_from_ru(string: str) -> str:
    """! Transliterate word from russian to english

    Этот метод используется для транслитерации строки
    с русского на анлгийский

    @param string Строка на русском языке

    @return Строка на английском языке
    """
    return transliterate.translit(string, 'ru', reversed=True)


def get_current_semester() -> int:
    """! Auto choose current semestr

    Этот метод используется для определения текущего семестра обучения
    
    @return Числовое значение текущего семестра
    """
    month = datetime.now().month
    if 1 < month < 9:
        return 2
    return 1


def get_extension(filename: str) -> str:
    """! Get file extension from link 
    Этот метод используется для получения расширения файла
    
    @param filename Ссылка на файл

    @return Расширение файла без точки
    """
    index = filename.rfind('.')
    if index < 0:
        return None
    return filename[index+1:]
