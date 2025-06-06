from datetime import datetime
from ..data import Position
from ..order import Order
from typing import Union

class StatisticTracker():
    '''
    Base class for tracking strategy statistics.

    Subclass this to implement custom tracking logic using the `start`, `update`, and `end` lifecycle hooks.
    Subclass this to also impliment custom tracked statistic queries and string generation methods using the `getStats` and `getStatsStr` functions.
    '''

    def __init__(self, statisticID: str):
        '''
        Initializes the statistic tracker with a unique ID.

        :param statisticID: A unique identifier for this statistic tracker.
        '''

        self.statisticID: str = statisticID

        self.ticker: Union[None, str] = None
        self.dateTime: Union[None, datetime] = None
        self.open: Union[None, float] = None
        self.close: Union[None, float] = None
        self.low: Union[None, float] = None
        self.high: Union[None, float] = None
        self.volume: Union[None, int] = None
        self.portfolioCash: float = 0.0
        self.portfolioValue: float = 0.0
        self.commissionPercent: float = 0.0
        self.slippagePercent: float = 0.0
        self.positions: dict[str:Position] = {}
        self.orders: list[Order] = []
        self.openOrders: list[Order] = []
        self.closedOrders: list[Order] = []

    def __updateStatisticsInfo__(self, ticker: str,
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
        Internal method to update the current market and portfolio state for the statistic tracker.

        :param ticker: The current ticker symbol being processed.
        :param dateTime: The current timestamp of the data point.
        :param open: The opening price of the ticker.
        :param close: The closing price of the ticker.
        :param low: The lowest price of the ticker.
        :param high: The highest price of the ticker.
        :param volume: The volume traded for the ticker.
        :param portfolioCash: The current cash available in the portfolio.
        :param portfolioValue: The total value of the portfolio including positions.
        :param commissionPercent: The commission percentage for trading.
        :param slippagePercent: The max slippage percentage for trading.
        :param positions: The current positions held in the portfolio.
        :param orders: The list of all orders issued during this time step.
        :param openOrders: The list of currently open orders.
        :param closedOrders: The list of closed orders.
        
        :return: None
        '''

        self.ticker = ticker
        self.dateTime = dateTime
        self.open = open
        self.close = close
        self.low = low
        self.high = high
        self.volume = volume
        self.portfolioCash = portfolioCash
        self.portfolioValue = portfolioValue
        self.commissionPercent = commissionPercent
        self.slippagePercent = slippagePercent
        self.positions = positions
        self.orders = orders
        self.openOrders = openOrders
        self.closedOrders = closedOrders

    def start(self) -> None:
        '''
        Called once at the beginning of the backtest to initialize state.

        :return: None
        '''

        pass

    def update(self) -> None:
        '''
        Called on each timestep (e.g., for each bar or candle) to update the statistics.

        :return: None
        '''

        pass

    def end(self) -> None:
        '''
        Called once at the end of the backtest to finalize calculations or summaries.

        :return: None
        '''

        pass

    def getStats(self) -> any:
        '''
        Returns the computed statistics.

        :return: The result of the tracked statistic, type varies depending on the implementation.
        '''

        return None

    def getStatsStr(self) -> str:
        '''
        Returns a human-readable string representation of the tracked statistics.
        This string will be used in the statistics report string generation from the
        current testing engine being used.

        :return: A string summary of the tracked statistics.
        '''

        return 'NONE'