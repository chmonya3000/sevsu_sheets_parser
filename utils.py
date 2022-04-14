import transliterate
from datetime import datetime


def transliteration_to_en_from_ru(string: str) -> str:
    """Транслитерация букв с русских на анлгийские"""
    return transliterate.translit(string, 'ru', reversed=True)


def get_current_semester() -> int:
    """Текущий семестр обучения"""
    month = datetime.now().month
    if 1 < month < 9:
        return 2
    return 1


def get_extension(filename: str) -> str:
    """Получение расширения файла"""
    index = filename.rfind('.')
    if index < 0:
        return None
    return filename[index+1:]
