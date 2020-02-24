from typing import List
from model import Measurement, MeasurementCollection
import os

BACKUP_FOLDER_NAME = 'backup'
BACKUP_FOLDER_PATH = './' + BACKUP_FOLDER_NAME


def _file(file_name: str, mode: str): return open(BACKUP_FOLDER_PATH + '/' + file_name + '.txt', mode, encoding='utf-8')


def _parse_measurement(measurement: str) -> Measurement:
    split_record = measurement.split(' ')
    time = split_record[0]
    temperature = float(split_record[2][:-3])
    humidity = float(split_record[4][:-1])
    return Measurement(time, temperature, humidity)


def create_directory_for_backup_files() -> str:
    if not os.path.exists(BACKUP_FOLDER_NAME):
        os.mkdir(BACKUP_FOLDER_NAME)
        return 'Directory "%s" created.' % BACKUP_FOLDER_NAME
    else:
        return 'Directory "%s" already exists.' % BACKUP_FOLDER_NAME


def write_content_to_backup_file(file_name: str, file_content: str) -> None:
    file = _file(file_name, 'w')
    file.write(file_content)
    file.close()


def read_measurements_of_backup_file(file_name: str) -> List[Measurement]:
    file = _file(file_name, 'r')
    measurements = [_parse_measurement(line[:-1]) for line in file]
    file.close()
    return measurements


def read_all_measurements() -> List[Measurement]:
    all_measurements = []
    for file_name in get_backup_file_names():
        all_measurements += read_measurements_of_backup_file(file_name)
    return all_measurements


def read_measurements_grouped_by_day() -> List[MeasurementCollection]:
    collections = []
    for file_name in get_backup_file_names():
        collections.append(MeasurementCollection(file_name, read_measurements_of_backup_file(file_name)))
    return collections


def get_backup_file_names() -> List[str]:
    backup_file_names = []
    for subdir, dirs, files in os.walk(BACKUP_FOLDER_PATH):
        for file in files:
            if subdir == BACKUP_FOLDER_PATH:
                backup_file_names.append(file[:-4])
    backup_file_names.sort()
    return backup_file_names


def count_backup_files() -> int:
    count = 0
    for subdir, dirs, files in os.walk(BACKUP_FOLDER_PATH):
        for _ in files:
            if subdir == BACKUP_FOLDER_PATH:
                count += 1
    return count
