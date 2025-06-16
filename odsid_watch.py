# from pathlib import Path
# from datetime import datetime, timezone
# obsid_folder = Path(r"c:\install\Obsidian\obsid")
# most_resent = max(obsid_folder.rglob("*"), key=lambda x: x.stat().st_mtime)
# d = datetime.fromtimestamp(most_resent.stat().st_mtime)
# print(most_resent, d)
import os
import zipfile
import argparse
from datetime import datetime


def files_changed_today(root_folder):
    today = datetime.now().date()
    changed_files = []

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).date()

            if file_mod_time == today:
                changed_files.append(file_path)
                print(f'Измененный файл: {os.path.relpath(file_path, root_folder)}')

    return changed_files


def zip_files(files, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            arcname = os.path.relpath(file, os.path.commonpath(files))
            zf.write(file, arcname)


def unzip_files(zip_file_path, output_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zf:
        zf.extractall(output_folder)
        print(f'Файлы из {zip_file_path} распакованы в {output_folder}')


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f'Создана директория: {directory}')


def main(action, root_folder, output_zip_path):
    ensure_directory_exists(output_zip_path)

    if action == 'p':
        changed_files = files_changed_today(root_folder)

        if changed_files:
            zip_file_name = os.path.join(output_zip_path, 'changed_files.zip')
            zip_files(changed_files, zip_file_name)
            print(f'ZIP-файл создан: {zip_file_name}')
        else:
            print('Сегодня не было найдено измененных файлов.')
    
    elif action == 'u':
        zip_file_name = os.path.join(output_zip_path, 'changed_files.zip')
        if os.path.exists(zip_file_name):
            unzip_folder = output_zip_path  # Или укажите другую папку для распаковки
            unzip_files(zip_file_name, unzip_folder)
        else:
            print(f'ZIP-файл не найден: {zip_file_name}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Упаковать или распаковать измененные файлы.')
    parser.add_argument('action', choices=['p', 'u'], help='p - упаковать изменившиеся файлы, u - распаковать архив')
    parser.add_argument('root_folder', help='Путь к папке для поиска изменившихся файлов')
    parser.add_argument('output_zip_path', help='Путь к папке для сохранения ZIP и распаковки')

    args = parser.parse_args()

    main(args.action, args.root_folder, args.output_zip_path)
