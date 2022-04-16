import table_parser as tp
import pandas as pd
import re


A = '2нед.                                                  31.01-6.02.22г'


def preprocessing_date(date: str) -> str:
    dates = [date for date in date.split() if re.search(r'\d{2}\.\d{2}', date)]
    symbols = '0123456789.'
    if len(dates) == 1:
        date = dates[0].split('-')[-1]
        result = ''
        for item in date:
            if item in symbols:
                result += item
        result = result.split('.')
        if int(result[0]) > 7:
            result[0] = str(int(result[0]) - 7)
        if len(result[-1]) == 2:
            result[-1] = str(2000 + int(result[-1]))
        result = '.'.join(result)
    else:
        result = 'Даты нет'
    return result


def main():
    print(preprocessing_date(A))
    #file = r'C:\Users\bobbert\Documents\Pythonist\sevsu_sheets_parser\tester.xlsx'
    #df = tp.read_raw_excel_file(file, sheet_name='test')
    #dates = df.iloc[0, :].tolist()
    #print(dates)
    #dates = [preprocessing_date(date) if not pd.isna(date) else date for date in dates]
    #print(dates)


if __name__ == '__main__':
    main()
