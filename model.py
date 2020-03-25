import datetime
from enum import Enum
from typing import NamedTuple, List
from abc import ABC


class MeasurementValue(ABC):
    def __init__(self, temperature: float, humidity: float):
        self.temperature = temperature
        self.humidity = humidity


class Measurement(MeasurementValue):
    def __init__(self, date: datetime.date, time: datetime.time, temperature: float, humidity: float):
        super().__init__(temperature, humidity)
        self.date = date
        self.time = time

    def datetime(self) -> datetime.datetime:
        return datetime.datetime.combine(self.date, self.time)


class MeasurementCollection(NamedTuple):
    tag: str
    measurements: List[Measurement]


class AggregationType(Enum):
    MIN = 1
    MAX = 2
    MEAN = 3


class MeasurementAggregation(MeasurementValue):
    def __init__(self, tag: str, type: AggregationType, temperature: float, humidity: float):
        super().__init__(temperature, humidity)
        self.tag = tag
        self.type = type
