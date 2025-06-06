from .statistic_tracker import StatisticTracker
from datetime import datetime
from ..data import Position
from ..order import Order

class StatisticsManager():
    '''
    Manager class for handling multiple StatisticTracker instances.

    Responsible for lifecycle management (start, update, end) of all registered statistic trackers,
    and for aggregating statistics retrieval by ID.
    '''

    def __init__(self):
        '''
        Initializes the StatisticsManager with an empty tracker list and a start flag.

        :return: None
        '''

        self.__statisticTrackers__: list[StatisticTracker] = []
        self.hasStarted: bool = False

    def addStatisticTracker(self, statisticTrackerClass: type[StatisticTracker]) -> None:
        '''
        Instantiate and add a new StatisticTracker of the given class to the manager.

        :param statisticTrackerClass: The StatisticTracker subclass to instantiate and track.
        :return: None
        '''

        self.__statisticTrackers__.append(statisticTrackerClass())

    def getStatistic(self, statisticID: str) -> any:
        '''
        Retrieve the computed statistic from the tracker with the matching statisticID.

        :param statisticID: The unique ID of the statistic to retrieve.
        :return: The statistic result, type varies depending on the StatisticTracker implementation.
        '''

        for statistic in self.__statisticTrackers__:
            if statistic.statisticID == statisticID:
                return statistic.getStats()

    def start(self) -> None:
        '''
        Calls the `start` lifecycle hook on all registered StatisticTracker instances.

        :return: None
        '''

        for statisticTracker in self.__statisticTrackers__:
            statisticTracker.start()

    def update(self) -> None:
        '''
        Calls the `update` method on all registered StatisticTracker instances.

        This method is intended to be called once per data point or time step to allow
        each statistic tracker to update internal state or metrics that do not require
        the full market/portfolio context provided by `updateStatisticsInfo`.

        :return: None
        '''
        
        for statisticTracker in self.__statisticTrackers__:
            statisticTracker.update()

    def updateStatisticsInfo(self, ticker: str,
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
        '''
        Updates all registered StatisticTrackers with the latest market and portfolio state.

        :param ticker: The current ticker symbol.
        :param dateTime: The current timestamp of the data point.
        :param open: The opening price.
        :param close: The closing price.
        :param low: The lowest price.
        :param high: The highest price.
        :param volume: The volume traded.
        :param portfolioCash: Current cash in the portfolio.
        :param portfolioValue: Current total portfolio value.
        :param commissionPercent: Commission percentage for trades.
        :param slippagePercent: Max slippage percentage for trades.
        :param positions: Dictionary of current positions keyed by ticker.
        :param orders: List of all orders issued at this timestep.
        :param openOrders: List of currently open orders.
        :param closedOrders: List of closed orders.
        
        :return: None
        '''

        for statisticTracker in self.__statisticTrackers__:
            statisticTracker.__updateStatisticsInfo__(ticker, 
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
        '''
        Calls the `end` lifecycle hook on all registered StatisticTracker instances.

        :return: None
        '''

        for statisticTracker in self.__statisticTrackers__:
            statisticTracker.end()