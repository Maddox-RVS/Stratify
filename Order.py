from datetime import datetime
from typing import Union
from enum import Enum

class FillStatus(Enum):
    PENDING: str = 'pending'
    FILLED: str = 'filled'
    PARTIALLY_FILLED: str = 'partially_filled'
    REJECTED: str = 'rejected'
    CANCELLED: str = 'cancelled'

class Order():
    def __init__(self, ticker: str, units: int):
        self.ticker: str = ticker
        self.units: int = units
        self.fillStatus: FillStatus = FillStatus.PENDING

        self.__opened__: Union[None, datetime] = None
        self.__closed__: Union[None, datetime] = None
        self.__boughtPrice__: Union[None, float] = None
        self.__sellPrice__: Union[None, float] = None

    def cancel(self):
        self.fillStatus = FillStatus.CANCELLED

class BuyOrder(Order):
    def __init__(self, ticker: str, units: int = 1):
        super().__init__(ticker, units)

class SellOrder(Order):
    def __init__(self, ticker: str, units: int = 1):
        super().__init__(ticker, units)

class CloseOrder(Order):
    def __init__(self, ticker, units: int = 1):
        super().__init__(ticker, units)