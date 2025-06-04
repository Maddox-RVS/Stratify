from datetime import datetime
from typing import Union
from enum import Enum

class FillStatus(Enum):
    '''
    Enum representing the current status of an order.
    '''

    PENDING: str = 'pending'
    FILLED: str = 'filled'
    PARTIALLY_FILLED: str = 'partially_filled'
    REJECTED: str = 'rejected'
    CANCELLED: str = 'cancelled'

class Order():
    '''
    Base class representing a trade order.
    '''

    def __init__(self, ticker: str, units: int):
        '''
        Initializes a new order.

        :param ticker: The stock ticker symbol.
        :param units: The number of units to trade.
        '''

        self.ticker: str = ticker
        self.units: int = units
        self.fillStatus: FillStatus = FillStatus.PENDING

        self.__opened__: Union[None, datetime] = None
        self.__closed__: Union[None, datetime] = None
        self.__boughtPrice__: Union[None, float] = None
        self.__sellPrice__: Union[None, float] = None

    def cancel(self) -> None:
        '''
        Cancels the order by setting its status to CANCELLED.
        
        :return: None
        '''

        self.fillStatus = FillStatus.CANCELLED

class BuyOrder(Order):
    '''
    Represents a buy order.
    '''

    def __init__(self, ticker: str, units: int = 1):
        '''
        Initializes a buy order.

        :param ticker: The stock ticker symbol.
        :param units: The number of units to buy.
        '''

        super().__init__(ticker, units)

class SellOrder(Order):
    '''
    Represents a sell order.
    '''
    
    def __init__(self, ticker: str, units: int = 1):
        '''
        Initializes a sell order.

        :param ticker: The stock ticker symbol.
        :param units: The number of units to sell.
        '''
        
        super().__init__(ticker, units)

class CloseOrder(Order):
    '''
    Represents an order to close a position by selling all held units.
    '''

    def __init__(self, ticker, units: int = 1):
        '''
        Initializes a close order.

        :param ticker: The stock ticker symbol.
        :param units: Placeholder value (will be overridden with full position units).
        '''

        super().__init__(ticker, units)