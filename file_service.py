from typing import List
import os

BACKUP_FOLDER_NAME = 'backup'
BACKUP_FOLDER_PATH = './' + BACKUP_FOLDER_NAME


def create_directory_for_backup_files() -> str:
    if not os.path.exists(BACKUP_FOLDER_NAME):
        os.mkdir(BACKUP_FOLDER_NAME)
        return 'Directory "%s" created.' % BACKUP_FOLDER_NAME
    else:
        return 'Directory "%s" already exists.' % BACKUP_FOLDER_NAME


def write_content_to_backup_file(file_name: str, file_content: str) -> None:
    file = open(BACKUP_FOLDER_PATH + '/' + file_name + '.txt', 'w', encoding='utf-8')
    file.write(file_content)


def get_backup_file_names() -> List[str]:
    backup_file_names = []
    for subdir, dirs, files in os.walk(BACKUP_FOLDER_PATH):
        for file in files:
            if subdir == BACKUP_FOLDER_PATH:
                backup_file_names.append(file[:-4])
    backup_file_names.sort()
    return backup_file_names
