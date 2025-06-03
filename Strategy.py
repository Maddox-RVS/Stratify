from order import Order, BuyOrder, SellOrder, CloseOrder
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

    def buy(self, units: int = 1) -> Order:
        order: BuyOrder = BuyOrder(self.ticker, units)
        self.orders.append(order)
        return order

    def sell(self, units: int = 1) -> Order:
        order: SellOrder = SellOrder(self.ticker, units)
        self.orders.append(order)
        return order

    def close(self) -> Order:
        order: CloseOrder = CloseOrder(self.ticker)
        self.orders.append(order)
        return order
    