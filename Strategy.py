from Order import Order, BuyOrder, SellOrder
from datetime import datetime
from typing import Union

class Strategy():
    def __init__(self):
        self.orders: list[Order] = []

        self.ticker: Union[None, str] = None
        self.dateTime: Union[None, datetime] = None
        self.open: Union[None, float] = None
        self.close: Union[None, float] = None
        self.low: Union[None, float] = None
        self.high: Union[None, float] = None
        self.volume: Union[None, int] = None

    def start(self):
        pass

    def next(self):
        pass

    def end(self):
        pass

    def buy(self, units: int = 1):
        order: BuyOrder = BuyOrder(self.ticker, units)
        self.orders.append(order)

    def sell(self, units: int = 1):
        order: SellOrder = SellOrder(self.ticker, units)
        self.orders.append(order)