from datetime import date
from typing import List, Optional

import plotly
import plotly.graph_objects as go
from plotly.graph_objs.scatter import Line
from plotly.subplots import make_subplots

from util import aggregation_service
import file_service
from model import MeasurementValue, MeasurementCollection
from plot import constants
from plot.model import PlotService


def _add_trace(fig: plotly.graph_objs.Figure, row: int, col: int, name: str, x_list: List[str],
               y_list: List[float], color: str) -> None:
    fig.add_trace(
        go.Scatter(
            x=x_list,
            y=y_list,
            mode="lines",
            name=name,
            line=Line(color=color)
        ),
        row=row, col=col,
    )


def _add_traces(fig: plotly.graph_objs.Figure, temperature_name: str, humidity_name: str, x_list: List[str],
                y_list: List[MeasurementValue], temperature_color: str, humidity_color: str) -> None:
    temperature_list = [value.temperature for value in y_list]
    humidity_list = [value.humidity for value in y_list]

    _add_temperature_trace(fig, temperature_name, x_list, temperature_list, temperature_color)
    _add_humidity_trace(fig, humidity_name, x_list, humidity_list, humidity_color)


def _add_temperature_trace(fig: plotly.graph_objs.Figure, name: str, x_list: List[str],
                           temperature_list: List[float], color: str) -> None:
    _add_trace(fig, 1, 1, name, x_list, temperature_list, color)


def _add_twenty_degrees_centigrade_trace(fig: plotly.graph_objs.Figure, x_list: List) -> None:
    _add_temperature_trace(fig, '20 °C', x_list, [20] * len(x_list), constants.TWENTY_DEGREES_CENTIGRADE_COLOR)


def _add_humidity_trace(fig: plotly.graph_objs.Figure, name: str, x_list: List[str],
                        humidity_list: List[float], color: str) -> None:
    _add_trace(fig, 2, 1, name, x_list, humidity_list, color)


def _init_plot() -> plotly.graph_objs.Figure:
    fig: plotly.graph_objs.Figure = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=[constants.TEMPERATURE_HEADING, constants.HUMIDITY_HEADING],
        specs=[[{"type": "scatter"}], [{"type": "scatter"}]]
    )
    fig.update_layout(
        height=800,
        showlegend=False,
        title_text=constants.TITLE,
        plot_bgcolor='white'
    )
    return fig


def _show_plot(fig: plotly.graph_objs.Figure) -> None:
    fig.show()
    # fig.write_html('plot.html', auto_open=True)


def _show_simple_plot(x_list: List[str], y_list: List[MeasurementValue]) -> None:
    temperature_list = [value.temperature for value in y_list]
    humidity_list = [value.humidity for value in y_list]

    fig: plotly.graph_objs.Figure = _init_plot()

    _add_twenty_degrees_centigrade_trace(fig, x_list)
    _add_temperature_trace(fig, constants.TEMPERATURE_HEADING, x_list, temperature_list, constants.TEMPERATURE_COLOR)
    _add_humidity_trace(fig, constants.HUMIDITY_HEADING, x_list, humidity_list, constants.HUMIDITY_COLOR)

    _show_plot(fig)


def _show_min_max_mean_plot(measurement_collections: List[MeasurementCollection]) -> None:
    mean_list = aggregation_service.mean_values(measurement_collections)
    min_list = aggregation_service.min_values(measurement_collections)
    max_list = aggregation_service.max_values(measurement_collections)

    x_list = [mean.tag for mean in mean_list]

    fig: plotly.graph_objs.Figure = _init_plot()

    _add_twenty_degrees_centigrade_trace(fig, x_list)
    _add_traces(fig, constants.MAX_TEMPERATURE_HEADING, constants.MAX_HUMIDITY_HEADING, x_list, max_list,
                constants.LIGHT_TEMPERATURE_COLOR, constants.LIGHT_HUMIDITY_COLOR)
    _add_traces(fig, constants.MEAN_TEMPERATURE_HEADING, constants.MEAN_HUMIDITY_HEADING, x_list, mean_list,
                constants.TEMPERATURE_COLOR, constants.HUMIDITY_COLOR)
    _add_traces(fig, constants.MIN_TEMPERATURE_HEADING, constants.MIN_HUMIDITY_HEADING, x_list, min_list,
                constants.LIGHT_TEMPERATURE_COLOR, constants.LIGHT_HUMIDITY_COLOR)

    fig.update_xaxes(type="category", row=1, col=1)
    fig.update_xaxes(type="category", row=2, col=1)
    fig.update_layout(showlegend=True)

    _show_plot(fig)


class PlotlyService(PlotService):

    def show_raw_plot(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> None:
        measurements = file_service.read_measurements(from_date, to_date)
        x_list = [str(measurement.datetime()) for measurement in measurements]
        _show_simple_plot(x_list, measurements)

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
        _show_min_max_mean_plot(measurement_collections)
