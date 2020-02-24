import statistics
from typing import List

import matplotlib.pyplot as plt

import file_service
from model import MeasurementCollection, MeasurementAggregation, AggregationType

TEMPERATURE_COLOR = 'tab:red'
LIGHT_TEMPERATURE_COLOR = 'mistyrose'
HUMIDITY_COLOR = 'tab:blue'
LIGHT_HUMIDITY_COLOR = 'lavender'


def _temperature_list(measurement_collection: MeasurementCollection) -> List[float]:
    return [measurement.temperature for measurement in measurement_collection.measurements]


def _humidity_list(measurement_collection: MeasurementCollection) -> List[float]:
    return [measurement.humidity for measurement in measurement_collection.measurements]


def _mean(measurement_collection: MeasurementCollection) -> MeasurementAggregation:
    return MeasurementAggregation(measurement_collection.tag, AggregationType.MEAN,
                                  statistics.mean(_temperature_list(measurement_collection)),
                                  statistics.mean(_humidity_list(measurement_collection)))


def _max(measurement_collection: MeasurementCollection) -> MeasurementAggregation:
    return MeasurementAggregation(measurement_collection.tag, AggregationType.MAX,
                                  max(_temperature_list(measurement_collection)),
                                  max(_humidity_list(measurement_collection)))


def _min(measurement_collection: MeasurementCollection) -> MeasurementAggregation:
    return MeasurementAggregation(measurement_collection.tag, AggregationType.MIN,
                                  min(_temperature_list(measurement_collection)),
                                  min(_humidity_list(measurement_collection)))


def create_plot() -> None:
    measurement_collections = file_service.read_measurements_grouped_by_day()

    fig, axs = plt.subplots(2, sharex=True)
    fig.suptitle('Temperature and humidity values')
    axs[0].set_title('Temperature (°C)')
    axs[1].set_title('Humidity (%)')

    daily_mean_list = [_mean(measurement_collection) for measurement_collection in measurement_collections]
    daily_min_list = [_min(measurement_collection) for measurement_collection in measurement_collections]
    daily_max_list = [_max(measurement_collection) for measurement_collection in measurement_collections]

    x_list = [daily_mean.tag for daily_mean in daily_mean_list]

    daily_mean_temperature_list = [daily_mean.temperature for daily_mean in daily_mean_list]
    daily_mean_humidity_list = [daily_mean.humidity for daily_mean in daily_mean_list]
    axs[0].plot(x_list, daily_mean_temperature_list, TEMPERATURE_COLOR)
    axs[1].plot(x_list, daily_mean_humidity_list, HUMIDITY_COLOR)

    daily_min_temperature_list = [daily_min.temperature for daily_min in daily_min_list]
    daily_min_humidity_list = [daily_min.humidity for daily_min in daily_min_list]
    axs[0].plot(x_list, daily_min_temperature_list, LIGHT_TEMPERATURE_COLOR)
    axs[1].plot(x_list, daily_min_humidity_list, LIGHT_HUMIDITY_COLOR)

    daily_max_temperature_list = [daily_max.temperature for daily_max in daily_max_list]
    daily_max_humidity_list = [daily_max.humidity for daily_max in daily_max_list]
    axs[0].plot(x_list, daily_max_temperature_list, LIGHT_TEMPERATURE_COLOR)
    axs[1].plot(x_list, daily_max_humidity_list, LIGHT_HUMIDITY_COLOR)

    first_days_of_month = [tag for tag in x_list if tag.endswith('-01')]
    indices = [x_list.index(tag) for tag in first_days_of_month]

    plt.xticks(indices, first_days_of_month)

    plt.show()
