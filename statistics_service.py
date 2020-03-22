import statistics
from datetime import date
from typing import List, Optional

import file_service
import filter_service
import print_service


def _print_statistics_for_list(values: List[float]) -> None:
    print('Mean: ' + str(statistics.mean(values)))
    print('Median: ' + str(statistics.median(values)))
    print('Min: ' + str(min(values)))
    print('Max: ' + str(max(values)))
    print('Standard deviation: ' + str(statistics.stdev(values)))


def show_statistics(from_date: Optional[date] = None, to_date: Optional[date] = None) -> None:
    print_service.print_heading('Statistics')

    measurements_in_interval = file_service.read_measurements(from_date, to_date)
    temperature_values_in_interval = [measurement.temperature for measurement in measurements_in_interval if
                                      filter_service.is_realistic_temperature_value(measurement.temperature)]
    humidity_values_in_interval = [measurement.humidity for measurement in measurements_in_interval]

    number_of_backup_files = file_service.count_backup_files()
    print_service.print_subheading('Number of backup files: ' + str(number_of_backup_files))
    number_of_backup_files_in_interval = file_service.count_backup_files(from_date, to_date)
    print('Number of backup files in interval: ' + str(number_of_backup_files_in_interval))
    number_of_measurements_in_interval = len(measurements_in_interval)
    print('Number of measurements in interval: ' + str(number_of_measurements_in_interval))

    print_service.print_subheading('Temperature (°C)')
    _print_statistics_for_list(temperature_values_in_interval)

    print_service.print_subheading('Humidity (%)')
    _print_statistics_for_list(humidity_values_in_interval)
