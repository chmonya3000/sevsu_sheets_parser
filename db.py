"""! @brief Класс для работы с базой данных"""
##
# @file db.py
#
# @brief Класс для работы с базой данных
#
# @section description_db Описание
# Полное управление базой данных начиная от создания таблиц, заканчивая считыванием записей
#
# @section libraries_db Модули
#   - sqlite3
#       - Модуль для работы с базой данных SQLite3  
# @section notes_db Заметки
#
# @section list_of_changes_db Список изменений
#   - Файл создан Нестеренко А.И. 17/04/2022
#   Добавлены методы:
#       - SQL.__init__
#       - SQL.create_table_request
#       - SQL.insert_datas_to_db
#       - SQL.return_all_from_db
#       - SQL.__craete_db_file
#       - SQL.__create_table
#       - SQL.create_db
#   - Добавлены методы Нестеренко А.И. 20/04/2022:
#       - SQL.execute_requests
#       - SQL.return_info
#
# @section author_db Авторы
# - Савинов В.В.
# - Нестеренко А.И.
#
# Copyright (c) 2022 ИРИБ.  All rights reserved.

from asyncio.windows_events import NULL
from xmlrpc.client import Boolean

import system
import sqlite3


class SQL:
    """! Class to work with SQL
    
    Класс работы с базой данныйх
    """

    def __init__(self):
        """! Constructor
        
        Конструктор класса

        @param self Объект класса(указывать не нужно)
        """
        ## День недели (максимум 16 символов)
        self.day = NULL
        ## Время пары (максимум 8 символов)
        self.lesson_number = NULL
        ## Название пары (максимум 128 символов)
        self.lesson = NULL
        ## Тип пары (максимум 4 символа)
        self.lesson_type = NULL
        ## Аудитория (максимум 8 символов)
        self.auditorium = NULL
        ## Номер недели (максимум 32 символов)
        self.week_number = NULL
        ## Название группы (максимум 16 символов)
        self.group_name = NULL
        ## Имя преподавателя (максимум 32 символов)
        self.teacher_name = NULL

        self.path = NULL

    def create_table_request(name: str, **kwargs: dict) -> str:
        """! Create table request

        Создание SQL запроса на создание таблицы

        @params name Название таблицы
        @params **kwargs Словарь типа {Название поля} : {Тип поля}

        @return SQL запрос для создания таблицы в БД
        """
        request = f'CREATE TABLE IF NOT EXISTS {name}(\nID INTEGER PRIMARY KEY AUTOINCREMENT'
        for param, type in kwargs.items():
            request = request + f',\n{str(param)} {type}'
        request = request + ');'
        return request

    def insert_datas_to_db(self, name: str, **kwargs: dict) -> str:
        """! Insert datas to database
        
        Добавить запись в таблицу

        @params name Название таблицы
        @params **kwargs Словарь типа {Название поля} : {Значение}

        @return SQL запрос для добавления записей в БД
        """
        request = f'INSERT INTO {name} ('
        for param, value in kwargs.items():
            request = request + f'{str(param)}, '
        request = request[:-2] + ')\nVALUES ('
        for param, value in kwargs.items():
            request = request + f"'{value}', "
        request = request[:-2] + ');'
        return request

    def return_all_from_db(self, name: str) -> str:
        """! Return all values from table
        
        Возвращает все записи с таблицы

        @param name Название таблицы

        @return SQL запрос для возврата всех данных с таблицы
        """
        return f'SELECT * FROM {name};'

    def __craete_db_file(self) -> str:
        """! Create database file
        
        Создает файл базы данных

        @return Абсолютный путь к созданной базе данных
        """
        return system.create_file('Database', 'test', 'sqlite3')

    def __create_table(db_file: str):
        """! Create table in database

        Создает таблицу для хранения данных о прах

        @param db_file Путь к файлу
        """
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(SQL.create_table_request('pair', day='VARCHAR(16)', lesson_number='INT', week_number='VARCHAR(32)',
                                             group_name='VARCHAR(16)', teacher_name='VARCHAR(64)',
                                             lesson='VARCHAR(128)', lesson_type='VARCHAR(4)', auditorium='VARCHAR(8)'))
        conn.commit()

    def execute_requests(self, request: str) -> None:
        """! Execute INSERT method

        Сохраняет данные в таблицу по указанному SQL запросу

        @param request INSERT запрос
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(request)
        conn.commit()

    def return_info(self, request: str) -> list:
        """! Execute SELECT method

        Возвращает инфу с таблицы по указанному запросу

        @param request SELECT запрос

        @return Список со всеми подходящими под запрос записями
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(request)
        return type(cur.fetchall())

    def create_db(self) -> Boolean:
        """! Create whole database with all needed tables
        
        Создает базу данных со всеми нужными таблицами

        @return Возвращает True если все успешно созданно и 
        False если есть ошибки при создании
        """
        try:
            self.path = SQL.__craete_db_file(self)
            SQL.__create_table(self.path)
            return True
        except:
            return False


def main():
    """! Function to test and debug code

    Эта функция используется для отладки написанного кода
    """

    SQL.create_db()
    a = SQL.insert_datas_to_db('pair', day='1', lesson_number=2, week_number='3', group_name='4', teacher_name='5',
                               lesson='6', lesson_type='7', auditorium='8')
    SQL.execute_requests(a)
    a = SQL.return_all_from_db('pair')
    print(SQL.return_info(a))


if __name__ == "__main__":
    main()
