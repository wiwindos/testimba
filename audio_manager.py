# audio_manager.py

import os

# Путь к папке, которую мы мониторим
folder_path = 'audio'

# Путь к папке, в которую перемещаем обработанные файлы
archive_path = 'archive'

# Функция для перемещения файла в папку "archive"
def move_to_archive(file_name):
    source_path = os.path.join(folder_path, file_name)
    target_path = os.path.join(archive_path, file_name)
    os.rename(source_path, target_path)
