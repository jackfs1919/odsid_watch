# from pathlib import Path
# from datetime import datetime, timezone
# obsid_folder = Path(r"c:\install\Obsidian\obsid")
# most_resent = max(obsid_folder.rglob("*"), key=lambda x: x.stat().st_mtime)
# d = datetime.fromtimestamp(most_resent.stat().st_mtime)
# print(most_resent, d)
import os
import zipfile
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


def main(root_folder, output_zip_path):
    changed_files = files_changed_today(root_folder)

    if changed_files:
        zip_file_name = os.path.join(output_zip_path, 'changed_files.zip')
        zip_files(changed_files, zip_file_name)
        print(f'ZIP-файл создан: {zip_file_name}')
    else:
        print('Сегодня не было найдено измененных файлов.')

    # Распаковка ZIP-файла
    unzip_folder = output_zip_path  # Или укажите другую папку для распаковки
    unzip_files(zip_file_name, unzip_folder)


if __name__ == "__main__":
    # Замените пути на ваши
    root_folder = r"c:\install\Obsidian\obsid"
    output_zip_path = r"c:\install\Obsidian\zip" 
    main(root_folder, output_zip_path)
