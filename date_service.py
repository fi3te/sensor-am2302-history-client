import datetime
from typing import NamedTuple, Optional


class IsoCalendar(NamedTuple):
    year: int
    week_number: int
    weekday: int


def _lstrip_zero(number_str: str) -> int:
    number_str = number_str.lstrip('0')
    return int(number_str) if len(number_str) > 0 else 0


def file_name_to_iso_calendar(file_name: str) -> IsoCalendar:
    file_date = file_name_to_date(file_name)
    return IsoCalendar(*file_date.isocalendar())


def file_name_to_date(file_name: str) -> datetime.date:
    return datetime.datetime.strptime(file_name, '%Y-%m-%d').date()


def parse_time(time: str) -> datetime.time:
    split_time = time.split(':')
    hour = _lstrip_zero(split_time[0])
    minute = _lstrip_zero(split_time[1])
    second = _lstrip_zero(split_time[2])
    return datetime.time(hour, minute, second)


def file_name_in_interval(file_name: str, from_date: Optional[datetime.date] = None,
                          to_date: Optional[datetime.date] = None) -> bool:
    date = file_name_to_date(file_name)
    return (not from_date or from_date <= date) and (not to_date or date <= to_date)
