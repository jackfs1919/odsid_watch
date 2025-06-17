"""
Набор функций для работы с облаком.
Для работы требует установки библиотеки:
pip install webdavclient3 cryptocode
"""

from pathlib import Path

from cryptocode import decrypt
from webdav3.client import Client


def decrypt_word(word: str, psw: str) -> str:
    """
    Дешифрование слова, переданного в функцию.
    """
    return decrypt(word, psw)


def authorize(psw: str) -> (Client, bool):
    """
    Авторизация в облаке. Декодирование логина и пароля.
    Создание клиента с авторизацией.
    Возвращение клиента из функции для использования в других функциях.
    """
    datas = [x.strip() for x in open('setting.ini', 'r', encoding='utf-8') if x.strip()]
    login = decrypt_word(datas[0], psw)
    password = decrypt_word(datas[1], psw)
    if login:
        data = {
            'webdav_hostname': "https://webdav.cloud.mail.ru",
            'webdav_login': login,
            'webdav_password': password
        }

        client = Client(data)
        return client
    return False


def check_setting() -> bool:
    """
    Проверка существования файла настроек.
    """
    if not Path('setting.ini').exists():
        return False
    return True


def connect_cloud_folder(client: Client, path: str) -> dict:
    """
    Читает содержимое переданной директории в облаке.
    Возвращает словарь с полученными значениями.
    """
    my_files = client.list(path, get_info=True)
    return my_files


def create_cloud_folder(client, path: str) -> bool:
    """
    Создание директории в облаке. Возвращает True,
    если создание директории прошло успешно.
    """
    return client.mkdir(path)


def delete_cloud_folder(client: Client, path: str):
    """
    Удаление переданной директории в облаке.
    """
    client.clean(path)


def upload_cloud_file(client: Client, remote_path: str, local_path: str):
    """
    Загрузка файла в облако.
    """
    client.upload_sync(remote_path, local_path)


def download_cloud_file(client: Client, remote_path: str, local_path: str) -> bool:
    """
    Скачивание файла из облака.
    """
    client.download_sync(remote_path, local_path)
    return True


def move_cloud_object(client: Client, remote_path_from: str, remote_path_to: str):
    """
    Перемещение файла в облаке.
    """
    client.move(remote_path_from, remote_path_to)


def copy_cloud_object(client: Client, remote_path_from: str, remote_path_to: str):
    """
    Копирование файла в облаке.
    """
    client.copy(remote_path_from, remote_path_to)
