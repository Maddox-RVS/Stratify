from datetime import datetime
from ..data import Position
from ..order import Order
from typing import Union

class StatisticTracker():
    def __init__(self, statisticID: str):
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

    def __updateStatistics__(self, ticker: str,
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
        pass

    def update(self) -> None:
        pass

    def end(self) -> None:
        pass

    def getStats(self) -> any:
        return None

    def getStatsStr() -> str:
        return ''