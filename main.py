import bs4
import requests


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


def get_extension(file):
    i = len(file) - 1
    extension = ""
    while file[i] != '.':
        extension += file[i]
        i -= 1
    return "".join(reversed(extension))
    

def get_file(url, extension):
    f = open("test.xls", "wb")
    file = requests.get(url + "/images/raspis/2021-2022/1%20SEMESTR/irib/distant/IRIb%2007_12%20(1).xls")
    f.write(file.content)
    f.close()


def main():
    soup = get_current_block(URL, HEADERS)
    institutes = get_institute(soup)
    for i in institutes:
        for j in get_files_urls(i):
            print(i.find("h3").text + "\t" + get_extension(j))
    #get_file(SEVSU)


if __name__ == "__main__":
    main()
