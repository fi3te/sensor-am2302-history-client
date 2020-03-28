from datetime import date
from typing import List, Callable, Optional

import matplotlib.pyplot as plt
from matplotlib import figure, axes

from util import aggregation_service
import file_service
from model import MeasurementCollection, MeasurementValue
from plot import constants
from plot.model import PlotService

MAX_NUMBER_OF_XTICKS = 5


def _default_filter_tags_for_xticks(tags: List[str]) -> List[str]:
    return _spaced_tags(tags, MAX_NUMBER_OF_XTICKS)


def _init_plot(x_list: List[str]) -> (figure.Figure, List[axes.Axes]):
    fig, axs = plt.subplots(2, sharex='all')
    fig.suptitle(constants.TITLE)
    axs[0].set_title(constants.TEMPERATURE_HEADING)
    axs[1].set_title(constants.HUMIDITY_HEADING)
    axs[0].plot(x_list, [20] * len(x_list), constants.TWENTY_DEGREES_CENTIGRADE_COLOR)
    return fig, axs


def _plot_values(axs: List[axes.Axes], x_list: List[str], y_list: List[MeasurementValue], temperature_color: str,
                 humidity_color: str) -> None:
    temperature_list = [value.temperature for value in y_list]
    humidity_list = [value.humidity for value in y_list]
    axs[0].plot(x_list, temperature_list, temperature_color)
    axs[1].plot(x_list, humidity_list, humidity_color)


def set_xticks(x_list: List[str],
               filter_tags_for_xticks: Callable[[List[str]], List[str]] = _default_filter_tags_for_xticks) -> None:
    tags = filter_tags_for_xticks(x_list)
    indices = [x_list.index(tag) for tag in tags]
    plt.xticks(indices, tags)


def _show_min_max_mean_plot(measurement_collections: List[MeasurementCollection],
                            filter_tags_for_xticks: Callable[
                                [List[str]], List[str]] = _default_filter_tags_for_xticks) -> None:
    mean_list = aggregation_service.mean_values(measurement_collections)
    min_list = aggregation_service.min_values(measurement_collections)
    max_list = aggregation_service.max_values(measurement_collections)

    x_list = [mean.tag for mean in mean_list]

    fig, axs = _init_plot(x_list)

    _plot_values(axs, x_list, mean_list, constants.TEMPERATURE_COLOR, constants.HUMIDITY_COLOR)
    _plot_values(axs, x_list, min_list, constants.LIGHT_TEMPERATURE_COLOR, constants.LIGHT_HUMIDITY_COLOR)
    _plot_values(axs, x_list, max_list, constants.LIGHT_TEMPERATURE_COLOR, constants.LIGHT_HUMIDITY_COLOR)

    set_xticks(x_list, filter_tags_for_xticks)

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


class MatplotlibService(PlotService):

    def show_raw_plot(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> None:
        measurements = file_service.read_measurements(from_date, to_date)
        x_list = [str(measurement.datetime()) for measurement in measurements]

        fig, axs = _init_plot(x_list)

        _plot_values(axs, x_list, measurements, constants.TEMPERATURE_COLOR, constants.HUMIDITY_COLOR)

        set_xticks(x_list)

        plt.show()

    def show_hourly_mean_plot(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> None:
        measurement_collections = file_service.read_measurements_grouped_by_hour(from_date, to_date)
        _show_min_max_mean_plot(measurement_collections)

    def show_daily_mean_plot(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> None:
        measurement_collections = file_service.read_measurements_grouped_by_day(from_date, to_date)
        _show_min_max_mean_plot(measurement_collections)

    def show_weekly_mean_plot(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> None:
        measurement_collection = file_service.read_measurements_grouped_by_week(from_date, to_date)
        _show_min_max_mean_plot(measurement_collection)

    def show_monthly_mean_plot(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> None:
        measurement_collections = file_service.read_measurements_grouped_by_month(from_date, to_date)
        _show_min_max_mean_plot(measurement_collections, lambda tags: _evenly_spaced(tags, MAX_NUMBER_OF_XTICKS))
