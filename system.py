import os
import requests


def make_directory(filename: str):
    """Создание папки"""
    if os.path.exists(filename):
        return
    os.mkdir(filename)


def get_file(path: str, name: str, url: str, extension: str) -> None:
    """Сохранение таблицы расписания"""
    make_directory(f'General/{path}')
    f = open(f'General/{path}/{name}.{extension}', "wb")
    file = requests.get(url)
    f.write(file.content)
    f.close()
