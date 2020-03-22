import datetime
import os
from typing import List, Optional

import date_service
from model import Measurement, MeasurementCollection

BACKUP_FOLDER_NAME = 'backup'
BACKUP_FOLDER_PATH = './' + BACKUP_FOLDER_NAME


def _file(file_name: str, mode: str): return open(BACKUP_FOLDER_PATH + '/' + file_name + '.txt', mode, encoding='utf-8')


def _parse_measurement(measurement: str, date: datetime.date) -> Measurement:
    split_record = measurement.split(' ')
    time = date_service.parse_time(split_record[0])
    temperature = float(split_record[2][:-3])
    humidity = float(split_record[4][:-1])
    return Measurement(date, time, temperature, humidity)


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
    date = date_service.file_name_to_date(file_name)
    measurements = [_parse_measurement(line[:-1], date) for line in file]
    file.close()
    return measurements


def read_measurements(from_date: Optional[datetime.date] = None,
                      to_date: Optional[datetime.date] = None) -> List[Measurement]:
    all_measurements = []
    for file_name in get_backup_file_names_without_file_extension():
        if date_service.file_name_in_interval(file_name, from_date, to_date):
            all_measurements += read_measurements_of_backup_file(file_name)
    return all_measurements


def read_measurements_grouped_by_day(from_date: Optional[datetime.date] = None,
                                     to_date: Optional[datetime.date] = None) -> List[MeasurementCollection]:
    collections = []
    for file_name in get_backup_file_names_without_file_extension():
        if date_service.file_name_in_interval(file_name, from_date, to_date):
            collections.append(MeasurementCollection(file_name, read_measurements_of_backup_file(file_name)))
    return collections


def read_measurements_grouped_by_month(from_date: Optional[datetime.date] = None,
                                       to_date: Optional[datetime.date] = None) -> List[MeasurementCollection]:
    measurements_of_month_dictionary = {}
    for file_name in get_backup_file_names_without_file_extension():
        if date_service.file_name_in_interval(file_name, from_date, to_date):
            month_key = file_name[:-3]
            month_collection = measurements_of_month_dictionary.get(month_key, None)
            if month_collection is None:
                month_collection = MeasurementCollection(month_key, [])
                measurements_of_month_dictionary[month_key] = month_collection
            month_collection.measurements.extend(read_measurements_of_backup_file(file_name))
    return [value for key, value in measurements_of_month_dictionary.items()]


def read_measurements_grouped_by_week(from_date: Optional[datetime.date] = None,
                                      to_date: Optional[datetime.date] = None) -> List[MeasurementCollection]:
    measurement_of_week_dictionary = {}
    for file_name in get_backup_file_names_without_file_extension():
        if date_service.file_name_in_interval(file_name, from_date, to_date):
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


def count_backup_files(from_date: Optional[datetime.date] = None, to_date: Optional[datetime.date] = None) -> int:
    count = 0
    for subdir, dirs, files in os.walk(BACKUP_FOLDER_PATH):
        for file in files:
            if subdir == BACKUP_FOLDER_PATH:
                file_name = file[:-4]
                if date_service.file_name_in_interval(file_name, from_date, to_date):
                    count += 1

    return count
