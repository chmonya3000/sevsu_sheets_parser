import bs4
import requests
import os
import transliterate
from datetime import datetime

URL = "https://www.sevsu.ru/univers/shedule"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
SEVSU = "https://www.sevsu.ru"


def get_current_block(url, headers):
    html = requests.get(url=url, headers=headers)
    soup = bs4.BeautifulSoup(html.text, "lxml")
    return soup.find("div", class_="su-column-content")


def get_institute(soup):
    return [i for i in soup.find_all("div", class_="su-spoiler")]


def get_files_urls(soup):
    files = soup.find("div", class_= "su-clearfix").find_all("a")
    return [i.get("href") for i in files]


def get_extension(filename: str):
    """Получение расширение файлаа"""
    index = filename.rfind('.')
    if index < 0:
        return
    return filename[index+1:]
    

def get_file(path, name, url, file_path, extension):
    make_directory("general/" + str(path))
    f = open("general/"+str(path) + "/" + str(name) + str(extension), "wb")
    file = requests.get(url + file_path)
    f.write(file.content)
    f.close()


def make_directory(name):
    if os.path.exists(name):
        return
    os.mkdir(name)


def translit_words(string):
    return transliterate.translit(string, "ru", reversed=True)


def current_semester():
    month = datetime.now().month
    if 1 < month < 9:
        return 2
    return 1


def get_first_semester(array):
    print(array)


def main():
    semester = current_semester()
    soup = get_current_block(URL, HEADERS)
    institutes = get_institute(soup)
    for x in institutes:
        temp_p_div = [el.text.replace('\xa0', '') for el in x.find("div", class_="su-clearfix").find_all("p")]
        temp_p_div = [el for el in range(len(temp_p_div)) if 'семестр' in temp_p_div[el]]
        if semester == 1:
            if len(temp_p_div) == 2:
                temp_p_div = get_files_urls(x)[:temp_p_div[-1] - temp_p_div[0] - 1]
            get_first_semester(temp_p_div)
        else:
            if len(temp_p_div) == 2:
                temp_p_div = get_files_urls(x)[temp_p_div[-1] - temp_p_div[0] - 1:]
            get_first_semester(temp_p_div)
        for j, y in enumerate(get_files_urls(x)):

            extension = get_extension(y)
            if extension == ".xls" or extension == ".xlsx":
                directory_name = translit_words(x.find("h3").text)
                get_file(directory_name, j, SEVSU, y, extension)
    #get_file(SEVSU)


if __name__ == "__main__":
    main()
