"""! @brief Методы для парсинга расписания ГПИ"""
##
# @file gpi.py
#
# @brief Методы для парсинга расписания ГПИ.
#
# @section description_gpi Описание
# Один из py файлов для таргетного парсинга конкретного института
#
# @section libraries_gpi Модули
#   - datetime
#       - Работа со временем
#   - numpy
#       - Мощный инструмент для математических вычислений
#   - pandas
#       - Парсинг Excel таблиц
#   - re
#       - Модуль для работы с регулярными выражениями    
#   
# @section notes_gpi Заметки
#
# @section list_of_changes_gpi Список изменений
#   - Файл создан Савинов В.В. 15/04/2022
#
# @section author_gpi Авторы
# - Савинов В.В.
# - Нестеренко А.И.
#
# Copyright (c) 2022 ИРИБ.  All rights reserved.

from datetime import datetime, timedelta
import numpy as np
import table_parser as tp
import pandas as pd
import re


def preprocessing_date(date: str, difference=-6, symbols='0123456789.') -> datetime:
    """! Get correct format date of statr study week

    Получение корректной даты начала учебной недели
    
    @param date Дата
    @param difference Разница между входным параметром и возвращаемым значением (в днях)
    @param symbols Символы разрешенные для использования в дате

    @return Дата начала учебной недели
    """
    dates = [date for date in date.split() if re.search(r'\d{2}\.\d{2}', date)]
    if len(dates) == 1:
        date = dates[0].split('-')[-1]
        result = ''.join([item for item in date if item in symbols])
        result = [r for r in result.split('.') if r]
        if len(result) == 3:
            if len(result[-1]) == 2:
                result[-1] = str(2000 + int(result[-1]))
        else:
            result = result + [str(datetime.now().year)]
        result = '.'.join(result)
        result = datetime.strptime(result, '%d.%m.%Y')
        if result.weekday() == 5:
            result = result + timedelta(days=difference + 1)
        else:
            result = result + timedelta(days=difference)
        result = result.strftime('%d.%m.%Y')
    else:
        result = np.nan
    return result


def main():
    """! Function to test and debug code

    Эта функция используется для отладки написанного кода
    """
    file = r'C:\Users\bobbert\Documents\Pythonist\sevsu_sheets_parser\test1111.xlsx'
    df = tp.read_raw_excel_file(file, sheet_name='test')
    df.iloc[0, :] = pd.Series([preprocessing_date(el) if not pd.isna(el) else el for el in df.iloc[0, :]])
    df = tp.remove_irrelevant_dates(df)
    df.to_excel('tester1111.xlsx', sheet_name='test', header=False, index=False)


if __name__ == '__main__':
    main()
