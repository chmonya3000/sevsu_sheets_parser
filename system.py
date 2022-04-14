import os
import requests


def make_directory(filename: str):
    """! mkdir
    
    Этот метод используется для проверки директории на наличие,
    если таковой нет, то будет создана

    @param filename Название директории  
    """
    if os.path.exists(filename):
        return
    os.mkdir(filename)


def save_file(path: str, name: str, url: str, extension: str) -> None:
    """! Save shedule file
    
    Этот метод используется для сохранения расписания в директорию института

    @param path Название директории внутри папки General
    @param name Название файла
    @param url  Ссылка на файл
    @param extension    Расширение файла 
    """
    make_directory(f'General/{path}')
    f = open(f'General/{path}/{name}.{extension}', "wb")
    file = requests.get(url)
    f.write(file.content)
    f.close()
