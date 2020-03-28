import statistics
from typing import List

from util import filter_service
from model import MeasurementCollection, MeasurementAggregation, AggregationType


def _temperature_list(measurement_collection: MeasurementCollection) -> List[float]:
    return filter_service.impute_temperature_values_with_mean_of_surroundings(
        [measurement.temperature for measurement in measurement_collection.measurements])


def _humidity_list(measurement_collection: MeasurementCollection) -> List[float]:
    return [measurement.humidity for measurement in measurement_collection.measurements]


def max_value(measurement_collection: MeasurementCollection) -> MeasurementAggregation:
    return MeasurementAggregation(measurement_collection.tag, AggregationType.MAX,
                                  max(_temperature_list(measurement_collection)),
                                  max(_humidity_list(measurement_collection)))


def max_values(measurement_collections: List[MeasurementCollection]) -> List[MeasurementAggregation]:
    return [max_value(measurement_collection) for measurement_collection in measurement_collections]


def mean_value(measurement_collection: MeasurementCollection) -> MeasurementAggregation:
    return MeasurementAggregation(measurement_collection.tag, AggregationType.MEAN,
                                  statistics.mean(_temperature_list(measurement_collection)),
                                  statistics.mean(_humidity_list(measurement_collection)))


def mean_values(measurement_collections: List[MeasurementCollection]) -> List[MeasurementAggregation]:
    return [mean_value(measurement_collection) for measurement_collection in measurement_collections]


def min_value(measurement_collection: MeasurementCollection) -> MeasurementAggregation:
    return MeasurementAggregation(measurement_collection.tag, AggregationType.MIN,
                                  min(_temperature_list(measurement_collection)),
                                  min(_humidity_list(measurement_collection)))


def min_values(measurement_collections: List[MeasurementCollection]) -> List[MeasurementAggregation]:
    return [min_value(measurement_collection) for measurement_collection in measurement_collections]
