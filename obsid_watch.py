# from pathlib import Path
# from datetime import datetime, timezone
# obsid_folder = Path(r"c:\install\Obsidian\obsid")
# most_resent = max(obsid_folder.rglob("*"), key=lambda x: x.stat().st_mtime)
# d = datetime.fromtimestamp(most_resent.stat().st_mtime)
# print(most_resent, d)
import os
import zipfile
import argparse
import time

start_script = time.perf_counter()
d = 1 # количество дней, за которые надо отследить изменения
os.system("taskkill /im Obsidian.exe /f")
# Определение путей для разных компьютеров
COMPUTER_PATHS = {
    'DAY': {
        'input_folder': 'c:\\install\\Obsidian\\obsid'
    },
    'KOMPUTER': {
        'input_folder': 'c:\\Program Files\\Obsidian\\obsid'
    }
}


def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def find_changed_files(root_folder):
    changes = []  # Список для хранения изменений

    for root, dirs, files in os.walk(root_folder):
        for d in dirs:
            # Сохраняем каталоги, начинающиеся с точки
            if d.startswith('.'):
                changes.append(os.path.join(root, d))

        for f in files:
            file_path = os.path.join(root, f)
            # Здесь вы можете добавить свою логику для проверки изменений файла
            # Например, проверка по времени последнего изменения
            if os.path.getmtime(file_path) > time.time() - 86400 * d:  # файлы измененные за последний день
                changes.append(file_path)
                print(f'Измененный файл: {os.path.relpath(file_path, root_folder)}')

    return changes


def zip_changed_files(changed_files, output_zip_path):
    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_LZMA, compresslevel=9, allowZip64=True) as zipf:
        for file in changed_files:
            zipf.write(file, os.path.relpath(file, os.path.dirname(changed_files[0])))
    print("Файлы упакованы")


def unzip_files(zip_file_name, output_folder):
    with zipfile.ZipFile(zip_file_name, 'r') as zipf:
        zipf.extractall(output_folder)
    print("Файлы распакованы")


def main(action, root_folder, output_zip_path):
    output_folder = root_folder
    ensure_directory_exists(output_zip_path)

    if action == 'p':
        changed_files = find_changed_files(root_folder)
        if changed_files:
            zip_file_name = os.path.join(output_zip_path, 'changed_files.zip')
            zip_changed_files(changed_files, zip_file_name)
            print(f'Упаковано {len(changed_files)} изменившихся файлов в {zip_file_name}')
        else:
            print('Нет изменившихся файлов для упаковки.')
    if action == 'u':
        zip_file_name = os.path.join(output_zip_path, 'changed_files.zip')
        if os.path.exists(zip_file_name):
            unzip_files(zip_file_name, output_folder)
            print(f'Распаковано в {output_folder}')
            os.remove(zip_file_name)
            print('Файл дельты удален')
        else:
            print(f'ZIP-файл не найден: {zip_file_name}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Упаковать или распаковать измененные файлы.')
    parser.add_argument('action', choices=['p', 'u'], help='p - упаковать изменившиеся файлы, u - распаковать архив')
    parser.add_argument('--path', help='Пользовательский путь к папке', default=None)
    parser.add_argument('--d', help='Количество дней для отслеживания изменений', default=1)

    args = parser.parse_args()

    # Получаем имя компьютера
    computer_name = os.getenv('COMPUTERNAME')
    output_zip_path = "o:\\install\\obsid"
    paths = COMPUTER_PATHS.get(computer_name)
    if paths:
        root_folder = args.path if args.path else paths['input_folder']
        d = args.d if args.d else 1
    else:
        print(f'Нет настроенных путей для компьютера: {computer_name}')
        exit(1)

    main(args.action, root_folder, output_zip_path)
    print(f'время исполнения {round((time.perf_counter() - start_script), 2)} сек.')
    time.sleep(5)
