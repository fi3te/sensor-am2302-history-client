import statistics
from typing import List

import file_service
import filter_service
import print_service


def _print_statistics_for_list(values: List[float]) -> None:
    print('Mean: ' + str(statistics.mean(values)))
    print('Median: ' + str(statistics.median(values)))
    print('Min: ' + str(min(values)))
    print('Max: ' + str(max(values)))
    print('Standard deviation: ' + str(statistics.stdev(values)))


def show_statistics() -> None:
    print_service.print_heading('Statistics')

    all_measurements = file_service.read_all_measurements()
    number_of_measurements = len(all_measurements)
    number_of_backup_files = file_service.count_backup_files()
    temperature_values = [measurement.temperature for measurement in all_measurements if
                          filter_service.is_realistic_temperature_value(measurement.temperature)]
    humidity_values = [measurement.humidity for measurement in all_measurements]

    print_service.print_subheading('Number of backup files: ' + str(number_of_backup_files))
    print('Number of measurements: ' + str(number_of_measurements))

    print_service.print_subheading('Temperature (°C)')
    _print_statistics_for_list(temperature_values)

    print_service.print_subheading('Humidity (%)')
    _print_statistics_for_list(humidity_values)
