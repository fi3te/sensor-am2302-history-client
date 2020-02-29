import statistics
from typing import List

DEFAULT_IMPUTATION_TEMPERATURE_VALUE = 20.0
MIN_REALISTIC_TEMPERATURE_VALUE = 10.0


def is_realistic_temperature_value(value: float) -> bool:
    return value >= MIN_REALISTIC_TEMPERATURE_VALUE


def impute_temperature_values_with_mean_of_surroundings(values: List[float]) -> List[float]:
    for index, value in enumerate(values):
        if not is_realistic_temperature_value(value):
            surrounding_values = []
            if index > 0 and is_realistic_temperature_value(values[index - 1]):
                surrounding_values.append(values[index - 1])
            if index + 1 < len(values) and is_realistic_temperature_value(values[index + 1]):
                surrounding_values.append(values[index + 1])
            if len(surrounding_values) == 0:
                surrounding_values.append(DEFAULT_IMPUTATION_TEMPERATURE_VALUE)
            mean = statistics.mean(surrounding_values)
            values[index] = mean
    return values
