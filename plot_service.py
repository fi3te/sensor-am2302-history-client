import statistics
from typing import List, Callable

import matplotlib.pyplot as plt

import file_service
import filter_service
from model import MeasurementCollection, MeasurementAggregation, AggregationType

TWENTY_DEGREES_CENTIGRADE_COLOR = 'lightgrey'
TEMPERATURE_COLOR = 'tab:red'
LIGHT_TEMPERATURE_COLOR = 'mistyrose'
HUMIDITY_COLOR = 'tab:blue'
LIGHT_HUMIDITY_COLOR = 'lavender'
MAX_NUMBER_OF_XTICKS = 5


def _temperature_list(measurement_collection: MeasurementCollection) -> List[float]:
    return filter_service.impute_temperature_values_with_mean_of_surroundings(
        [measurement.temperature for measurement in measurement_collection.measurements])


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


def _show_min_max_mean_plot(measurement_collections: List[MeasurementCollection],
                            filter_tags_for_xticks: Callable[[List[str]], List[str]] = lambda tags: _spaced_tags(tags,
                                                                                                                 MAX_NUMBER_OF_XTICKS)) -> None:
    fig, axs = plt.subplots(2, sharex=True)
    fig.suptitle('Temperature and humidity values')
    axs[0].set_title('Temperature (°C)')
    axs[1].set_title('Humidity (%)')

    mean_list = [_mean(measurement_collection) for measurement_collection in measurement_collections]
    min_list = [_min(measurement_collection) for measurement_collection in measurement_collections]
    max_list = [_max(measurement_collection) for measurement_collection in measurement_collections]

    x_list = [mean.tag for mean in mean_list]

    axs[0].plot(x_list, [20] * len(x_list), TWENTY_DEGREES_CENTIGRADE_COLOR)

    mean_temperature_list = [mean.temperature for mean in mean_list]
    mean_humidity_list = [mean.humidity for mean in mean_list]
    axs[0].plot(x_list, mean_temperature_list, TEMPERATURE_COLOR)
    axs[1].plot(x_list, mean_humidity_list, HUMIDITY_COLOR)

    min_temperature_list = [min_item.temperature for min_item in min_list]
    min_humidity_list = [min_item.humidity for min_item in min_list]
    axs[0].plot(x_list, min_temperature_list, LIGHT_TEMPERATURE_COLOR)
    axs[1].plot(x_list, min_humidity_list, LIGHT_HUMIDITY_COLOR)

    max_temperature_list = [max_item.temperature for max_item in max_list]
    max_humidity_list = [max_item.humidity for max_item in max_list]
    axs[0].plot(x_list, max_temperature_list, LIGHT_TEMPERATURE_COLOR)
    axs[1].plot(x_list, max_humidity_list, LIGHT_HUMIDITY_COLOR)

    tags = filter_tags_for_xticks(x_list)
    indices = [x_list.index(tag) for tag in tags]

    plt.xticks(indices, tags)

    plt.show()


def _spaced_tags(tags: List[str], number_of_elements: int) -> List[str]:
    if len(tags) <= number_of_elements:
        return tags
    else:
        number_of_tags = len(tags)
        return [tags[int(x * (number_of_tags - 1) / (number_of_elements - 1))] for x in range(number_of_elements)]


def _evenly_spaced(tags: List[str], max_number_of_elements: int) -> List[str]:
    if len(tags) <= max_number_of_elements:
        return tags
    else:
        number_of_tags = len(tags)
        every_nth = round(number_of_tags / max_number_of_elements)
        return [tag for num, tag in enumerate(tags) if num % every_nth == 0]


def show_daily_mean_plot() -> None:
    measurement_collections = file_service.read_measurements_grouped_by_day()
    _show_min_max_mean_plot(measurement_collections)


def show_weekly_mean_plot() -> None:
    measurement_collection = file_service.read_measurements_grouped_by_week()
    _show_min_max_mean_plot(measurement_collection)


def show_monthly_mean_plot() -> None:
    measurement_collections = file_service.read_measurements_grouped_by_month()
    _show_min_max_mean_plot(measurement_collections, lambda tags: _evenly_spaced(tags, MAX_NUMBER_OF_XTICKS))
