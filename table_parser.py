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
# - xlrd openpyxl
#   - Интсрументы для чтения xls и xlsx фалйов
# - datetime
#   - Получение текущего времени
#
# @section notes_table_parser Заметки
#
# @section list_of_changes_table_parser Список изменений
#   - Файл создан Савинов В.В. 14/04/2022
#   - Добавлена doxygen документация Нестеренко А.И. 15/04/2022
#   - Добавлены методы Савинов В.В. 17/04/2022:
#       - parse_date_study_week
#       - date_row_index
#       - group_row_index
#       - info_column_index
#       - get_date_indexes
#       - read_formatting_excel_file_xls
#       - delete_uninformative_table_information
#       - get_week_start_date
#       - update_informative_table_information
#
# @section author_utils Авторы
# - Савинов В.В.
# - Нестеренко А.И.
#
# Copyright (c) 2022 ИРИБ.  All rights reserved.

from datetime import datetime, timedelta, time
import pandas as pd
import utils
import xlrd
import numpy as np
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


def parse_date_study_week(date: str) -> list:
    """! Get list of study week

    Получение дат в удовлетворимом виде

    @param  date Строка с датами

    @return Список дат учебных недель
    """
    date = [date for date in date.split('  ') if date.replace(' ', '')]
    date = [date.split('-')[0].replace(' ', '') for date in date]
    date = [utils.update_format_date(date) for date in date]
    return date


def date_row_index(dataframe: pd.DataFrame) -> int:
    """! Get date row index
    Индекс строки, содержющей даты занятия (с данного индекса начинается расписание)
    
    @param dataframe Excel таблица

    @return Индекс строки с датой
    """
    columns = get_table_size(dataframe)[1]
    date_index = 0
    for i in range(columns):
        try:
            date_index = dataframe.iloc[:, i].index[
                dataframe.iloc[:, i].str.replace(' ', '').str.contains(r'\d{2}\.\d{2}', regex=True, na=False)][0]
            break
        except AttributeError:
            continue
        except IndexError:
            continue
    return date_index


def group_row_index(dataframe: pd.DataFrame) -> int:
    """! Get study group row index

    Индекс строки, содержющей группы, у которых прововодятся занятия

    @param dataframe Excel таблица

    @return Индекс строки с названиями учебных групп
    """
    columns = get_table_size(dataframe)[1]
    group_index = 0
    for i in range(columns):
        try:
            group_index = dataframe.iloc[:, i].index[
                dataframe.iloc[:, i].str.replace(' ', '').str.contains(r'\-\d{2}\-\d\-', regex=True, na=False)][0]
            break
        except AttributeError:
            continue
        except IndexError:
            continue
    return group_index


def info_column_index(dataframe: pd.DataFrame) -> int:
    """! Get start column index

    Индекс столбца, с которого начинается расписание
    
    @param dataframe Excel таблица

    @return Индекс столбца начала таблицы с расписанием
    """
    columns = get_table_size(dataframe)[1]
    initial_column = 0
    for i in range(columns):
        try:
            dataframe.iloc[:, i].str.contains(r'\-\d{2}\-\d\-', regex=True, na=False)
            break
        except AttributeError:
            initial_column += 1
    return initial_column


def get_date_indexes(dataframe: pd.DataFrame) -> list:
    """! Get indexes of all study week in sheet

    Индексы дат, для разделения таблицы
    
    @param dataframe Excel таблица

    @return Список индексов с датами учебных недель
    """
    rows, columns = get_table_size(dataframe)
    result = []
    for i in range(columns):
        try:
            group_indexes = dataframe.iloc[:, i].index[
                dataframe.iloc[:, i].str.replace(' ', '').str.contains(r'\d{2}\.\d{2}', regex=True, na=False)]
            if group_indexes.tolist():
                result += group_indexes.tolist()
                break
        except AttributeError:
            continue
        except IndexError:
            continue
    # if len(result) > 1:
    #    result += [rows]
    # else:
    #    result += ['xyu']
    return result


def read_formatting_excel_file_xls(filename: str, sheet_name: str) -> pd.DataFrame:
    """! Fill same cells in xls file

    Заполнение объединенных ячеек таблицы Excel расширения xls
    
    @param filename Имя файла
    @param sheet_name Имя листа

    @return Excel таблица с разделенными ячейками, что были объединены в одну
    """
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
    """! Remove useless row and column
    
    Удаление неинформативных столбцов и строк
    
    @param dataframe Excel таблица
    @param chunk Количество ячеек для просмотра

    @return Excel таблица без ненужной информации
    """
    date_index = date_row_index(dataframe.head(chunk))
    group_index = group_row_index(dataframe.head(chunk))
    initial_column = info_column_index(dataframe.head(chunk))
    dataframe = dataframe.drop(range(date_index), axis=0)
    dataframe = dataframe.drop(range(initial_column), axis=1)
    days = dataframe.iloc[2, :].index[dataframe.iloc[2, :].str.replace(' ', '').str.lower() == 'понедельник'][1:]
    dataframe = dataframe.drop(days, axis=1)
    pairs = dataframe.iloc[2, :].index[dataframe.iloc[2, :].str.replace(' ', '').str.lower() == '1пара'][1:]
    dataframe = dataframe.drop(pairs, axis=1)
    pairs = dataframe.iloc[2, :].index[dataframe.iloc[2, :] == time(8, 30)][1:]
    dataframe = dataframe.drop(pairs, axis=1)
    dataframe = dataframe.reset_index(drop=True)
    return dataframe


def get_week_start_date(date: str, difference=-6) -> str:
    """! Get week start date
    
    Дата начала учебной недели
    
    @param date Дата
    @param difference Разница между принимаемой и возвращаемой датой(в днях)

    @return Дата с разницей во времени на difference дней
    """
    date = datetime.strptime(date, '%d.%m.%Y')
    date = date + timedelta(days=difference)
    date = date.strftime('%d.%m.%Y')
    return date


def update_informative_table_information(dataframe: pd.DataFrame) -> pd.DataFrame:
    """! Update informative column

    Обновление информативных столбцов в таблице
    
    @param dataframe Excel таблица
    
    @return Отформотированная Excel таблица
    """
    dataframe.iloc[0, :] = dataframe.iloc[0, :].fillna(method='ffill')
    dataframe.iloc[1, :] = pd.Series([group if isinstance(group, str) else np.nan for group in dataframe.iloc[1, :].values]).fillna(method='ffill')
    dataframe.iloc[:, 0] = pd.Series(
        [day.replace(' ', '').lower() if not pd.isna(day) else day for day in dataframe.iloc[:, 0].values])
    dataframe.iloc[:, 1] = pd.Series(
        [day.replace(' ', '').lower() if not pd.isna(day) else day for day in dataframe.iloc[:, 1].values])
    dataframe.iloc[:, 2] = pd.Series(
        [day.strftime('%H:%M') if not pd.isna(day) else day for day in dataframe.iloc[:, 2].values])
    return dataframe


def remove_irrelevant_dates(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Удаление прошедших недель"""
    rows, _ = get_table_size(dataframe)
    dataframe.loc[rows] = dataframe.iloc[0, :].copy()
    dataframe.iloc[-1] = pd.Series([get_key_difference_date(date) if not pd.isna(date) else date for date in dataframe.iloc[-1].values])
    useless_indexes = dataframe.iloc[-1].index[dataframe.iloc[-1] > 0]
    dataframe = dataframe.drop(useless_indexes, axis=1)
    dataframe = dataframe.iloc[:rows, :]
    dataframe = dataframe.dropna(axis=1, thresh=3)
    return dataframe


def get_key_difference_date(date: str) -> int:
    """! Get difference between date

    Нахождение разницы между текущей датой и даты начала учебной недели

    @param date Дата начала учебной недели

    @return Количество дней между началом учебной недели и нынешним днем
    """
    study_week_date = datetime.strptime(date, '%d.%m.%Y').date()
    return (datetime.now().date() - study_week_date).days


def get_information_for_database_from_table(dataframe: pd.DataFrame, i: int, j: int) -> tuple:
    """Получение данных из ячейки таблицы"""
    if pd.isna(dataframe.iloc[i, j]):
        day = dataframe.iloc[i, 0].capitalize()
        number = int(dataframe.iloc[i, 1][0])
        week_date = datetime.strptime(dataframe.iloc[0, j], '%d.%m.%Y').date()
        group = dataframe.iloc[1, j]
        teacher, lesson, lesson_type, classroom = np.nan
    else:
        print('Ячейка полная дурак')
    return day, number, week_date, group, teacher, lesson, lesson_type, classroom


def main():
    """! Function to test and debug code

    Эта функция используется для отладки написанного кода
    """
    file = r'General\Gumanitarno-pedagogicheskij institut\1.xls'
    sheets = get_sheet_names_from_table(file)
    for sheet in sheets:
        df = read_formatting_excel_file_xls(file, sheet)
        # df.to_excel('test0.xlsx', sheet_name='test', header=False, index=False)
        df = delete_uninformative_table_information(df)
        # df.to_excel('test1.xlsx', sheet_name='test', header=False, index=False)
        df = update_informative_table_information(df)
        # df.to_excel('test2.xlsx', sheet_name='test', header=False, index=False)
        import department.gpi as gpi
        df.iloc[0, :] = pd.Series([gpi.preprocessing_date(el) if not pd.isna(el) else el for el in df.iloc[0, :]])
        df = remove_irrelevant_dates(df)
        # df.to_excel('test3.xlsx', sheet_name='test', header=False, index=False)
        get_information_for_database_from_table(df, 7, 3)




        #indexes = get_date_indexes(df)
        #print(indexes)
        #result = df.iloc[indexes[0]:indexes[1], :]
        #for index in range(1, len(indexes) - 1):
        #    temp = df.iloc[indexes[index]:indexes[index + 1], :]
        #    temp.reset_index(drop=True, inplace=True)
        #    temp.to_excel(f'test1111{index}.xlsx', sheet_name='test', header=False, index=True)
        #    result = pd.merge(result, temp, right_index=True, left_index=True)
        #result.to_excel('tester111.xlsx', sheet_name='test', header=False, index=False)
        break


if __name__ == '__main__':
    main()
