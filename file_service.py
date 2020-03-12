import os
from typing import List

import date_service
from model import Measurement, MeasurementCollection

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
    for file_name in get_backup_file_names_without_file_extension():
        all_measurements += read_measurements_of_backup_file(file_name)
    return all_measurements


def read_measurements_grouped_by_day() -> List[MeasurementCollection]:
    collections = []
    for file_name in get_backup_file_names_without_file_extension():
        collections.append(MeasurementCollection(file_name, read_measurements_of_backup_file(file_name)))
    return collections


def read_measurements_grouped_by_month() -> List[MeasurementCollection]:
    measurements_of_month_dictionary = {}
    for file_name in get_backup_file_names_without_file_extension():
        month_key = file_name[:-3]
        month_collection = measurements_of_month_dictionary.get(month_key, None)
        if month_collection is None:
            month_collection = MeasurementCollection(month_key, [])
            measurements_of_month_dictionary[month_key] = month_collection
        month_collection.measurements.extend(read_measurements_of_backup_file(file_name))
    return [value for key, value in measurements_of_month_dictionary.items()]


def read_measurements_grouped_by_week() -> List[MeasurementCollection]:
    measurement_of_week_dictionary = {}
    for file_name in get_backup_file_names_without_file_extension():
        iso_calendar = date_service.file_name_to_iso_calendar(file_name)
        week_key = '%s.%s' % (iso_calendar.year, iso_calendar.week_number)
        week_collection = measurement_of_week_dictionary.get(week_key, None)
        if week_collection is None:
            week_collection = MeasurementCollection(week_key, [])
            measurement_of_week_dictionary[week_key] = week_collection
        week_collection.measurements.extend(read_measurements_of_backup_file(file_name))
    return [value for key, value in measurement_of_week_dictionary.items()]


def get_backup_file_names_without_file_extension() -> List[str]:
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
