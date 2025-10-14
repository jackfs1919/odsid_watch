import os
import pathlib
import shutil
import zipfile
import time
import logging
from termcolor import colored
import snoop

start_script = time.perf_counter()
os.system("taskkill /im Obsidian.exe /f")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
COMPUTER_PATHS = {
    'DAY': {
        'income_folder': 'c:\\install\\Obsidian\\obsid'
    },
    'KOMPUTER': {
        'income_folder': 'c:\\Program Files\\Obsidian\\obsid'
    }
}
ZIP_PATH = "o:\\install\\obsid"
zip_file = ""
computer_name = os.getenv('COMPUTERNAME')
paths = COMPUTER_PATHS.get(computer_name)


def five_sec_exit(s=1):
    time.sleep(5)
    exit(s)


def ensure_zipfile_exists(zip_path):
    global zip_file
    try:
        zip_file = list(pathlib.Path(zip_path).glob('*.zip'))[0].name
    except Exception as e:
        logger.error(colored(f'ZIP-файл не найден', 'red'))
        five_sec_exit()


def ensure_directory_exists(path):
    if not os.path.exists(path):
        logger.error(colored('Каталог архива недоступен', "red"))
        five_sec_exit()


def unzip_files(zip_file_name, output_folder):
    with zipfile.ZipFile(zip_file_name, 'r') as zipf:
        zipf.extractall(output_folder)
    logger.info(colored("Файлы распакованы", "green"))


def clear_directory(path):
    if not os.path.isdir(path):
        raise ValueError(colored(f"Указанный путь не является директорией: {path}", "red"))
    try:
        shutil.rmtree(path)
    except Exception as e:
        logger.error(colored(f"Не удалось удалить {path}: {e}"), "red")
        five_sec_exit()
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        logger.error(colored(f"Не удалось создать {path}: {e}"), "red")
        five_sec_exit()


@snoop
def main(root_folder, output_zip_path):
    output_folder = root_folder
    ensure_directory_exists(output_zip_path)
    ensure_zipfile_exists(ZIP_PATH)

    zip_file_name = os.path.join(output_zip_path, zip_file)
    if os.path.exists(zip_file_name):
        logger.info(colored(f'Найден архив {zip_file}', 'green'))
        clear_directory(output_folder)
        unzip_files(zip_file_name, output_folder)
        logger.info(colored(f'Распаковано в {output_folder}', 'green'))
        os.remove(zip_file_name)
        logger.info(colored('Файл архива удален', 'green'))
    else:
        logger.error(colored(f'ZIP-файл не найден: {zip_file_name}', 'red'))
        five_sec_exit()
        



if __name__ == "__main__":
    if paths:
        root_folder = paths['income_folder']
    else:
        logger.error(colored(f'Нет настроенных путей для компьютера: {computer_name}', "red"))
        five_sec_exit()
    main(root_folder, ZIP_PATH)
    logger.info(f'время исполнения {colored(str(round((time.perf_counter() - start_script), 2)), "green")} сек.')
    five_sec_exit(0)
