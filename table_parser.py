import pandas as pd
import utils
import xlrd


def get_sheet_names_from_table(filename: str) -> list:
    """Имена всех листов в документе Excel"""
    return pd.ExcelFile(filename).sheet_names


def get_table_size(dataframe: pd.DataFrame) -> tuple:
    """Размер таблицы на листе документа Excel"""
    rows, columns = dataframe.shape
    return rows, columns


def read_raw_excel_file(filename: str, sheet_name: str) -> pd.DataFrame:
    """Считывание информации из таблицы"""
    extension = utils.get_extension(filename)
    if extension == 'xlsx':
        return pd.read_excel(filename, sheet_name=sheet_name, header=None, engine='openpyxl')
    return pd.read_excel(filename, sheet_name=sheet_name, header=None, engine='xlrd')
