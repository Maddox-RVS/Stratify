from .statistic_tracker import StatisticTracker
from datetime import datetime
from ..data import Position
from ..order import Order

class StatisticsManager():
    def __init__(self):
        self.__statisticTrackers__: list[StatisticTracker] = []
        self.hasStarted: bool = False

    def addStatisticTracker(self, statisticTrackerClass: type[StatisticTracker]) -> None:
        self.__statisticTrackers__.append(statisticTrackerClass())

    def getStatistic(self, statisticID: str) -> any:
        for statistic in self.__statisticTrackers__:
            if statistic.statisticID == statisticID:
                return statistic.getStats()

    def start(self) -> None:
        for statisticTracker in self.__statisticTrackers__:
            statisticTracker.start()

    def updateStatistics(self, ticker: str,
                                dateTime: datetime,
                                open: float,
                                close: float,
                                low: float,
                                high: float,
                                volume: int,
                                portfolioCash: float,
                                portfolioValue: float,
                                commissionPercent: float,
                                slippagePercent: float,
                                positions: dict[str:Position],
                                orders: list[Order],
                                openOrders: list[Order],
                                closedOrders: list[Order]) -> None:
        for statisticTracker in self.__statisticTrackers__:
            statisticTracker.__updateStatistics__(ticker, 
                                                dateTime,
                                                open,
                                                close,
                                                low,
                                                high,
                                                volume,
                                                portfolioCash,
                                                portfolioValue,
                                                commissionPercent,
                                                slippagePercent,
                                                positions,
                                                orders,
                                                openOrders,
                                                closedOrders)
            
    def end(self) -> None:
        for statisticTracker in self.__statisticTrackers__:
            statisticTracker.end()