import pandas as pd
import utils


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


def parse_date_study_week(date):
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
            date_index = df.iloc[:, i].index[df.iloc[:, i].str.replace(' ', '').str.contains(r'\d{2}\.\d{2}', regex=True, na=False)][0]
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


if __name__ == '__main__':
    file = r'C:\Users\b402\Documents\sevsu_sheets_parser\General\Gumanitarno-pedagogicheskij institut\0.xlsx'
    sheets = get_sheet_names_from_table(file)
    for sheet in sheets:
        df = read_raw_excel_file(file, sheet)
        date_index = date_row_index(df.head(20))
        group_index = group_row_index(df.head(20))
        initial_column = info_column_index(df.head(20))
        df.drop(range(date_index), axis=0, inplace=True)
        df.drop(range(initial_column), axis=1, inplace=True)
        df.to_excel('test.xlsx', sheet_name='test', header=False, index=False)
        print(date_index, group_index, initial_column)
        break



