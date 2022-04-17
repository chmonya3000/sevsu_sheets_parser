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

import datetime
import pandas as pd
import utils
import xlrd
import openpyxl


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

    Считывание информации из таблицы без форматирования

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


def date_row_index(dataframe: pd.DataFrame) -> int:
    """Индекс строки, содержющей даты занятия (с данного индекса начинается расписание)"""
    columns = get_table_size(dataframe)[1]
    date_index = 0
    for i in range(columns):
        try:
            date_index = dataframe.iloc[:, i].index[dataframe.iloc[:, i].str.replace(' ', '').str.contains(r'\d{2}\.\d{2}', regex=True, na=False)][0]
            break
        except AttributeError:
            continue
        except IndexError:
            continue
    return date_index


def group_row_index(dataframe: pd.DataFrame) -> int:
    """Индекс строки, содержющей группы, у которых прововодятся занятия"""
    columns = get_table_size(dataframe)[1]
    group_index = 0
    for i in range(columns):
        try:
            group_index = df.iloc[:, i].index[df.iloc[:, i].str.replace(' ', '').str.contains(r'\-\d{2}\-\d\-', regex=True, na=False)][0]
            break
        except AttributeError:
            continue
        except IndexError:
            continue
    return group_index


def info_column_index(dataframe: pd.DataFrame) -> int:
    """Индекс столбца, с которого начинается расписание"""
    columns = get_table_size(dataframe)[1]
    initial_column = 0
    for i in range(columns):
        try:
            df.iloc[:, i].str.contains(r'\-\d{2}\-\d\-', regex=True, na=False)
            break
        except AttributeError:
            initial_column += 1
    return initial_column


def get_date_indexes(dataframe: pd.DataFrame) -> list:
    """Индексы дат, для разделения таблицы"""
    rows, columns = get_table_size(dataframe)
    result = []
    for i in range(columns):
        try:
            group_indexes = df.iloc[:, i].index[
                df.iloc[:, i].str.replace(' ', '').str.contains(r'\d{2}\.\d{2}', regex=True, na=False)]
            if group_indexes.tolist():
                result += group_indexes.tolist()
                break
        except AttributeError:
            continue
        except IndexError:
            continue
    #if len(result) > 1:
    #    result += [rows]
    #else:
    #    result += ['xyu']
    return result


def read_formatting_excel_file_xls(filename: str, sheet_name: str) -> pd.DataFrame:
    """Заполнение объединенных ячеек таблицы Excel расширения xls"""
    dataframe = read_raw_excel_file(filename=filename, sheet_name=sheet_name)
    rows, columns = get_table_size(dataframe)
    date_index = date_row_index(dataframe.head(20))
    workbook = xlrd.open_workbook(filename, formatting_info=True)
    sheet = workbook.sheet_by_name(sheet_name)
    for i, j, k, m in sheet.merged_cells:
        for row in range(i - 1, j - 1):
            for column in range(k, m):
                if date_index <= i <= rows:
                    if sheet.cell_value(i, k):
                        dataframe.loc[row + 1, column] = sheet.cell_value(i, k)
    return dataframe


def delete_uninformative_table_information(dataframe: pd.DataFrame, chunk=20) -> pd.DataFrame:
    """Удаление неинформативных столбцов и строк"""
    date_index = date_row_index(dataframe.head(chunk))
    group_index = group_row_index(dataframe.head(chunk))
    initial_column = info_column_index(dataframe.head(chunk))
    dataframe = dataframe.drop(range(date_index), axis=0)
    dataframe = dataframe.drop(range(initial_column), axis=1)
    days = dataframe.iloc[2, :].index[dataframe.iloc[2, :].str.replace(' ', '').str.lower() == 'понедельник'][1:]
    dataframe = dataframe.drop(days, axis=1)
    pairs = dataframe.iloc[2, :].index[dataframe.iloc[2, :].str.replace(' ', '').str.lower() == '1пара'][1:]
    dataframe = dataframe.drop(pairs, axis=1)
    pairs = dataframe.iloc[2, :].index[dataframe.iloc[2, :] == datetime.time(8, 30)][1:]
    dataframe = dataframe.drop(pairs, axis=1)
    dataframe = dataframe.reset_index(drop=True)
    return dataframe


def get_week_start_date(date: str, difference=-6) -> str:
    """Дата начала учебной недели"""
    date = datetime.datetime.strptime(date, '%d.%m.%Y')
    date = date + datetime.timedelta(days=difference)
    date = date.strftime('%d.%m.%Y')
    return date


def update_informative_table_information(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Обновление информативных столбцов в таблице"""
    dataframe.iloc[0, :] = dataframe.iloc[0, :].fillna(method='ffill')
    dataframe.iloc[1, :] = dataframe.iloc[1, :].fillna(method='ffill')
    dataframe.iloc[:, 0] = pd.Series([day.replace(' ', '').lower() if not pd.isna(day) else day for day in dataframe.iloc[:, 0].values])
    dataframe.iloc[:, 1] = pd.Series([day.replace(' ', '').lower() if not pd.isna(day) else day for day in dataframe.iloc[:, 1].values])
    dataframe.iloc[:, 2] = pd.Series([day.strftime('%H:%M') if not pd.isna(day) else day for day in dataframe.iloc[:, 2].values])
    return dataframe

def main():
    # a = get_sheet_names_from_table("1.xlsx")
    # b = read_raw_excel_file("1.xlsx", a[0])
    # print(b)
    file = r'C:\Users\bobbert\Documents\Pythonist\sevsu_sheets_parser\General\Gumanitarno-pedagogicheskij institut\1.xls'
    sheets = get_sheet_names_from_table(file)
    for sheet in sheets:
        df = read_formatting_excel_file_xls(file, sheet)
        df.to_excel('test0.xlsx', sheet_name='test', header=False, index=False)
        df = delete_uninformative_table_information(df)
        df = update_informative_table_information(df)
        df.to_excel('test.xlsx', sheet_name='test', header=False, index=False)
        indexes = get_date_indexes(df)
        print(indexes)
        #result = df.iloc[indexes[0]:indexes[1], :]
        #for index in range(1, len(indexes)-1):
        #    temp = df.iloc[indexes[index]:indexes[index + 1], :]
        #    temp.reset_index(drop=True, inplace=True)
        #    temp.to_excel(f'test{index}.xlsx', sheet_name='test', header=False, index=True)
        #    result = pd.merge(result, temp, right_index=True, left_index=True)
        #
        #result.to_excel('tester1.xlsx', sheet_name='test', header=False, index=False)
        break

if __name__ == '__main__':
    main()