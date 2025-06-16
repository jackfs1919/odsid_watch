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

os.system("taskkill /im Obsidian.exe /f")
# Определение путей для разных компьютеров
COMPUTER_PATHS = {
    'DAY': {
        'input_folder': 'c:\\install\\Obsidian\\obsid',
        'output_folder': 'c:\\install\\Obsidian\\obsid'
    },
    'COMPUTER2': {
        'input_folder': 'C:\\Path\\To\\Input\\Folder2',
        'output_folder': 'C:\\Path\\To\\Output\\Folder2'
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
            if os.path.getmtime(file_path) > time.time() - 86400:  # файлы измененные за последний день
                changes.append(file_path)

    return changes


def zip_changed_files(changed_files, output_zip_path):
    with zipfile.ZipFile(output_zip_path, 'w') as zipf:
        for file in changed_files:
            zipf.write(file, os.path.relpath(file, os.path.dirname(changed_files[0])))


def unzip_files(zip_file_name, output_folder):
    with zipfile.ZipFile(zip_file_name, 'r') as zipf:
        zipf.extractall(output_folder)


def main(action, root_folder, output_zip_path):
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
            unzip_files(zip_file_name, output_zip_path)
            print(f'Распаковано в {output_zip_path}')
        else:
            print(f'ZIP-файл не найден: {zip_file_name}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Упаковать или распаковать измененные файлы.')
    parser.add_argument('action', choices=['p', 'u'], help='p - упаковать изменившиеся файлы, u - распаковать архив')
    parser.add_argument('--path', help='Пользовательский путь к папке', default=None)

    args = parser.parse_args()

    # Получаем имя компьютера
    computer_name = os.getenv('COMPUTERNAME')
    output_zip_path = "o:\\install\\obsid"
    paths = COMPUTER_PATHS.get(computer_name)
    if paths:
        root_folder = args.path if args.path else paths['input_folder']
        output_folder = args.path if args.path else paths['output_folder']
    else:
        print(f'Нет настроенных путей для компьютера: {computer_name}')
        exit(1)

    main(args.action, root_folder, output_zip_path)
