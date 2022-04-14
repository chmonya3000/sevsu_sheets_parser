import bs4
import requests
import system
import html_parser
import utils

URL = "https://www.sevsu.ru/univers/shedule"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
SEVSU = "https://www.sevsu.ru"







def main():
    semester = utils.get_current_semester()
    institutes = html_parser.get_base_block(URL, HEADERS)

    for institute in institutes:
        temp_p_div = [el.text.replace('\xa0', ' ') for el in institute.find("div", class_="su-clearfix").find_all("p")]
        temp_p_div = [el for el in range(len(temp_p_div)) if 'семестр' in temp_p_div[el]]
        if semester == 1:
            if len(temp_p_div) == 2:
                temp_p_div = html_parser.get_files_url(institute)[:temp_p_div[-1] - temp_p_div[0] - 1]
            get_schedule_from_first_semester(temp_p_div)
        else:
            if len(temp_p_div) == 2:
                temp_p_div = html_parser.get_files_url(institute)[temp_p_div[-1] - temp_p_div[0] - 1:]
            get_schedule_from_second_semester(temp_p_div)
        for j, y in enumerate(html_parser.get_files_url(institute)):

            extension = utils.get_extension(y)
            if extension == ".xls" or extension == ".xlsx":
                directory_name = utils.transliteration_to_en_from_ru(x.find("h3").text)
                get_file(directory_name, j, SEVSU, y, extension)
    # get_file(SEVSU)


if __name__ == "__main__":
    main()
