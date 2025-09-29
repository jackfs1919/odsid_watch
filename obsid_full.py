import os
import zipfile
import time

start_script = time.perf_counter()
os.system("taskkill /im Obsidian.exe /f")
COMPUTER_PATHS = {
    'DAY': {
        'input_folder': 'c:\\install\\Obsidian\\obsid'
    },
    'KOMPUTER': {
        'input_folder': 'c:\\Program Files\\Obsidian\\obsid'
    }
}