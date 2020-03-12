from datetime import datetime
from typing import NamedTuple


class IsoCalendar(NamedTuple):
    year: int
    week_number: int
    weekday: int


def file_name_to_iso_calendar(file_name: str) -> IsoCalendar:
    file_date = datetime.strptime(file_name, '%Y-%m-%d').date()
    return IsoCalendar(*file_date.isocalendar())
