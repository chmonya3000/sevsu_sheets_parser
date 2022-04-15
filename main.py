import os
import pandas as pd
import table_parser as tp
import utils
import system


URL = "https://www.sevsu.ru/univers/shedule"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
BASE_URL = "https://www.sevsu.ru"


def main():
    files = system.get_path_schedule_files()

    for file in files:
        try:
            sheets = tp.get_sheet_names_from_table(file)
            for sheet in sheets:
                df = tp.read_raw_excel_file(file, sheet)
                print(df.shape)
        except ValueError:
            pass


if __name__ == "__main__":
    main()
