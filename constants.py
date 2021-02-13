from typing import Optional

import print_service

IP = '192.168.0.50'
PORT = 4000
BACKUP_FOLDER_PATH = './backup'


def add_parameters(func):
    global IP, PORT, BACKUP_FOLDER_PATH

    def wrapper(ip: str = IP,
                port: str = PORT,
                backup_folder_path: str = BACKUP_FOLDER_PATH) -> Optional:
        global IP, PORT, BACKUP_FOLDER_PATH
        if ip is not None:
            IP = ip
        if port is not None:
            PORT = port
        if backup_folder_path is not None:
            BACKUP_FOLDER_PATH = backup_folder_path

        print_service.print_subheading('Used parameters:')
        print(f'IP: {IP}')
        print(f'PORT: {PORT}')
        print(f'BACKUP_FOLDER_PATH: {BACKUP_FOLDER_PATH}')
        return func()

    return wrapper
