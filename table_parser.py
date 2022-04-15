"""! @brief Утилиты, которые могут понадобиться при работе"""
##
# @file table_parser.py
#
# @brief Парсер эксель таблиц
#
# @section description_table_parser Описание
#
# @section libraries_table_parser Модули
# - pandas
#   - Парсинг таблиц
# - xlrd
#   - Интсрумент для чтения xls фалйов
# - datetime
#   - Получение текущего времени
#
# @section notes_table_parser Заметки
#
# @section list_of_changes_table_parser Список изменений
#   - Файл создан Савинов В.В. 14/04/2022
#   - Добавлена doxygen документация Нестеренко А.И. 15/04/2022
#
# @section author_utils Авторы
# - Савинов В.В.
# - Нестеренко А.И.
#
# Copyright (c) 2022 ИРИБ.  All rights reserved.


import pandas as pd
import utils
import xlrd
import datetime


def get_sheet_names_from_table(filename: str) -> list:
    """! Get names of all lists in sheet

    Имена всех листов в документе Excel

    @param  filename Имя файла

    @return Список названий листов
    """
    return pd.ExcelFile(filename).sheet_names


def get_table_size(dataframe: pd.DataFrame) -> tuple:
    """! Get size of table list

    Размер таблицы на листе документа Excel

    @param  dataframe Лист таблицы

    @return (0) - количество строк (1) - количество столбцов
    """
    rows, columns = dataframe.shape
    return rows, columns


def read_raw_excel_file(filename: str, sheet_name: str) -> pd.DataFrame:
    """! Get info from file

    Считывание информации из таблицы

    @param  filename Имя файла
    @param  sheet_name Название листа

    @return Таблица данных с указанного листа
    """
    extension = utils.get_extension(filename)
    if extension == 'xlsx':
        return pd.read_excel(filename, sheet_name=sheet_name, header=None, engine='openpyxl')
    return pd.read_excel(filename, sheet_name=sheet_name, header=None, engine='xlrd')


def parse_date_study_week(dat : str) -> list:
    date = [date for date in date.split('  ') if date.replace(' ', '')]
    date = [date.split('-')[0].replace(' ', '') for date in date]
    date = [utils.update_format_date(date) for date in date]
    return date


def main():
    a = get_sheet_names_from_table("1.xlsx")
    b = read_raw_excel_file("1.xlsx", a[0])
    print(b)
    pass

if __name__ == '__main__':
    main()

