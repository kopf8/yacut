import os
import string


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'SECRET_KEY')
    TEMPLATE_FOLDER = 'templates'
    STATIC_FOLDER = 'static'


class Constants(object):
    ORIG_URL_MIN_LEN = 3
    ORIG_URL_MAX_LEN = 2000
    ORIG_URL_STR_LEN = 6
    SHORT_URL_MIN_LEN = 1
    SHORT_URL_MAX_LEN = 16
    SHORT_URL_LEN = 6
    SHORT_URL_FORMAT = r'^[a-zA-Z0-9]{1,16}$'
    SHORT_URL_CHARS = string.ascii_letters + string.digits
    API_DICT = {'url': 'original',
                'custom_id': 'short'}


class Messages(object):
    REQUIRED_FIELD = 'Обязательное поле'
    ORIG_URL_LEN = (f'Длина ссылки от {Constants.ORIG_URL_MIN_LEN} '
                    f'и до {Constants.ORIG_URL_MAX_LEN} знаков')
    ORIG_URL_FORMAT = 'Ссылка должна быть в формате URL'
    SHORT_URL_NOT_UNIQUE = (f'Предложенный вариант короткой ссылки'
                            f' уже существует.')
    SHORT_URL_LEN = (f'Длина должна быть от {Constants.SHORT_URL_MIN_LEN} '
                     f'и до {Constants.SHORT_URL_MAX_LEN} знаков')
    SHORT_URL_FORMAT = 'Допустимы только латинские символы и цифры'
    API_REQUIRED_BODY = 'Отсутствует тело запроса'
    API_REQUIRED_URL = '"url" является обязательным полем!'
    API_BAD_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки'
    API_SHORT_ID_NOT_FOUND = 'Указанный id не найден'
