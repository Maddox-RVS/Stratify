from ..statistic_tracker import StatisticTracker
from datetime import datetime
from typing import Union

class AnnualizedReturnTracker(StatisticTracker):
    DAYS_IN_TROPICAL_YEAR: float = 365.25

    def __init__(self):
        super().__init__('annualized_return')

        self.annualizedReturn: float = 0.0

        self.__initialValue__: float = 0.0
        self.__finalValue__: float = 0.0
        self.__startDate__: Union[None, datetime] = None
        self.__endDate__: Union[None, datetime] = None

    def start(self) -> None:
        self.__initialValue__ = self.portfolioValue
        self.__startDate__ = self.dateTime

    def end(self) -> None:
        self.__finalValue__ = self.portfolioValue
        self.__endDate__ = self.dateTime

        totalDays: int = (self.__endDate__ - self.__startDate__).days
        totalYears: int = totalDays / AnnualizedReturnTracker.DAYS_IN_TROPICAL_YEAR

        if totalYears <= 0: self.annualizedReturn = 0.0
        else:
            cagr: float = (self.__finalValue__ / self.__initialValue__) ** (1 / totalYears)
            self.annualizedReturn = cagr * 100

    def getStats(self) -> float:
        return self.annualizedReturn
    
    def getStatsStr(self) -> str:
        return f'Annualized Return: {round(self.annualizedReturn, 2)}%'