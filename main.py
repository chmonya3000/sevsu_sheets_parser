"""! @brief Основной файл для работы программы"""
##
# @file main.py
#
# @brief Основной файл для работы программы.
#
# @section description_main Описание
# Файл, который собрал в себе все методы для парсинга расписания.
#
# @section libraries_main Модули
#
# @section notes_main Заметки
#
# @section list_of_changes_main Список изменений
#   - Файл создан Нестеренко А.И. 14/04/2022
#
# @section author_main Авторы
# - Савинов В.В.
# - Нестеренко А.И.
#
# Copyright (c) 2022 ИРИБ.  All rights reserved.

from html_parser import get_base_block, get_institute_name, get_files_url, get_schedule_from_first_semester, get_schedule_from_second_semester
from table_parser import  get_sheet_names_from_table
from utils import get_extension, get_current_semester
from utils import transliteration_to_en_from_ru


URL = "https://www.sevsu.ru/univers/shedule"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
BASE_URL = "https://www.sevsu.ru"

def main():
    """! Function to test and debug code

    Эта функция используется для отладки написанного кода
    """
    base = get_base_block(URL, HEADERS)

    for item in base:
        name = transliteration_to_en_from_ru(get_institute_name(item))
        links = get_files_url(item)
        if get_current_semester() == 1:
            links = [BASE_URL + link for link in get_schedule_from_first_semester(item)]
        else:
            links = [BASE_URL + link for link in get_schedule_from_second_semester(item)]
        if links:
            for idx, link in enumerate(links):
                print(link)
                ext = get_extension(link)
                try:
                    b = get_sheet_names_from_table(f"General/{name}/{idx}.{ext}")
                    print(b)
                except ValueError:
                    print("Пошел нахуй ИФЭУ")


if __name__ == "__main__":
    main()
