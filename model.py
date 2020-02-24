from enum import Enum
from typing import NamedTuple, List


class Measurement(NamedTuple):
    time: str
    temperature: float
    humidity: float


class MeasurementCollection(NamedTuple):
    tag: str
    measurements: List[Measurement]


class AggregationType(Enum):
    MIN = 1
    MAX = 2
    MEAN = 3


class MeasurementAggregation(NamedTuple):
    tag: str
    type: AggregationType
    temperature: float
    humidity: float
