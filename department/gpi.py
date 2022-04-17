import datetime
import numpy as np
import table_parser as tp
import pandas as pd
import re


def preprocessing_date(date: str, difference=-6, symbols='0123456789.') -> datetime.datetime:
    """Получение корректной даты начала учебной недели"""
    dates = [date for date in date.split() if re.search(r'\d{2}\.\d{2}', date)]
    if len(dates) == 1:
        date = dates[0].split('-')[-1]
        result = ''.join([item for item in date if item in symbols])
        result = [r for r in result.split('.') if r]
        if len(result) == 3:
            if len(result[-1]) == 2:
                result[-1] = str(2000 + int(result[-1]))
        else:
            result = result + [str(datetime.datetime.now().year)]
        result = '.'.join(result)
        result = datetime.datetime.strptime(result, '%d.%m.%Y')
        result = result + datetime.timedelta(days=difference)
        result = result.strftime('%d.%m.%Y')
    else:
        result = np.nan
    return result


def main():
    file = r'C:\Users\bobbert\Documents\Pythonist\sevsu_sheets_parser\test.xlsx'
    df = tp.read_raw_excel_file(file, sheet_name='test')
    df.iloc[0, :] = pd.Series([preprocessing_date(el) if not pd.isna(el) else el for el in df.iloc[0, :]])
    df.to_excel('tester1.xlsx', sheet_name='test', header=False, index=False)


if __name__ == '__main__':
    main()
