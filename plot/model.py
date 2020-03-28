from abc import ABC, abstractmethod
from datetime import date
from typing import Optional


class PlotService(ABC):

    @abstractmethod
    def show_raw_plot(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> None:
        pass

    @abstractmethod
    def show_hourly_mean_plot(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> None:
        pass

    @abstractmethod
    def show_daily_mean_plot(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> None:
        pass

    @abstractmethod
    def show_weekly_mean_plot(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> None:
        pass

    @abstractmethod
    def show_monthly_mean_plot(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> None:
        pass
