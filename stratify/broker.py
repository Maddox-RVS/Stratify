from .order import Order, BuyOrder, SellOrder, CloseOrder, FillStatus
from dataclasses import dataclass
from datetime import datetime
from .data import TickerData
from .data import TickerFeed
from .data import Position
from typing import Union
import random

class BrokerStandard():
    '''
    A basic broker model that handles positions, orders, and cash management.
    '''

    def __init__(self):
        '''
        Initializes the broker.
        '''

        self.cash: float = 0.0
        self.commissionPercent: float = 0.0
        self.slippagePercent: float = 0.0

        self.__positions__: dict[str, Position] = {}

        self.__openOrders__: list[Order] = []
        self.__closedOrders__: list[Order] = []

        self.__dateTime__: Union[None, datetime] = None
        self.__tickerFeeds__: list[TickerFeed] = []

    def setCash(self, cashAmount: float) -> None:
        '''
        Sets the initial cash available in the broker.

        :param cashAmount: The amount of cash to set.
        :return: None
        '''

        self.cash = cashAmount

    def addCash(self, cashAmount: float) -> None:
        '''
        Adds cash to the broker account.

        :param cashAmount: The amount of cash to add.
        :return: None
        '''

        self.cash += cashAmount

    def setCommissionPercent(self, commisionPercent: float) -> None:
        '''
        Sets the commission percentage charged per trade.

        :param commisionPercent: Commission as a decimal (e.g., 0.01 for 1%).
        :return: None
        '''

        self.commissionPercent = commisionPercent

    def setSlippagePercent(self, slippagePercent: float) -> None:
        '''
        Sets the maximum slippage percentage to be applied during order execution.

        Slippage simulates the difference between the expected price and the actual price
        of an asset due to market conditions. The actual price used in trades will be 
        adjusted randomly between 0% and this value.

        :param slippagePercent: Maximum slippage as a decimal (e.g., 0.01 for 1%).
        :return: None
        '''
        
        self.slippagePercent = slippagePercent

    def getPosition(self, ticker) -> int:
        '''
        Gets the number of units held for a given ticker.

        :param ticker: The stock ticker symbol.
        :return: Number of units held for the ticker.
        '''

        tickers: list[str] = [position.ticker for position in self.__positions__]
        if ticker not in tickers: return 0
        for position in self.__positions__:
            if position.ticker == ticker:
                return position.units
            
    def getPortfolioValue(self) -> float:
        '''
        Calculates the total portfolio value (cash + value of positions).

        :return: The total portfolio value.
        '''

        value: float = self.cash

        timestampTickerFeed: TickerFeed = TickerFeed()
        for tickerFeed in self.__tickerFeeds__:
            for tickerData in tickerFeed:
                if tickerData.dateTime == self.__dateTime__:
                    timestampTickerFeed.append(tickerData)
        
        for tickerData in timestampTickerFeed:
            position: Position = self.__positions__.get(tickerData.ticker, Position(tickerData.ticker))
            value += tickerData.close * position.units

        return value
    
    def __closeOrder__(self, order: Order) -> None:
        '''
        Moves an order from open to closed.

        :param order: The order to close.
        :return: None
        '''

        order.__closedEndTime__ = datetime.now()
        self.__closedOrders__.append(order)
        self.__openOrders__.remove(order)

    def __rejectOrder__(self, order: Order) -> None:
        '''
        Removes an order entirely. Order is not counted as closed.

        :param order: The order to reject.
        :return: None
        '''

        self.__openOrders__.remove(order)

    def __executeBuyOrder__(self, tickerData: TickerData, order: Order) -> None:
        '''
        Executes a BuyOrder if sufficient cash and volume are available.

        :param tickerData: The market data used for order execution.
        :param order: The BuyOrder to execute.
        :return: None
        '''

        tickerVolume: int = tickerData.volume
        unitsNeeded: int = min(order.units, tickerVolume)
        randomSlippagePercent: float = (1 + random.uniform(0.0, self.slippagePercent))
        unitPrice: float = tickerData.close * randomSlippagePercent


        if (unitPrice * (1 + self.commissionPercent)) > self.cash or self.cash <= 0.0 or tickerVolume < 1 or order.units < 1:
            order.fillStatus = FillStatus.REJECTED
            self.__rejectOrder__(order)
            return
        
        tangibleUnits: int = min(unitsNeeded, int(self.cash / (unitPrice * (1 + self.commissionPercent))))
        orderCost: float = unitPrice * tangibleUnits
        commisionCash: float = orderCost * self.commissionPercent

        position: Position = self.__positions__.get(order.ticker, Position(order.ticker))
        tradeValue: float = orderCost + commisionCash
        self.cash -= tradeValue
        order._portfolioCashImpact = (-1.0 * tradeValue)
        position.units += tangibleUnits
        self.__positions__[order.ticker] = position

        order._unitsActuallyTraded = tangibleUnits
        order.fillStatus = FillStatus.PARTIALLY_FILLED if tangibleUnits < order.units else FillStatus.FILLED

        self.__closeOrder__(order)

    def __executeSellOrder__(self, tickerData: TickerData, order: Order) -> None:
        '''
        Executes a SellOrder based on current holdings.

        :param tickerData: The market data used for order execution.
        :param order: The SellOrder to execute.
        :return: None
        '''

        position: Position = self.__positions__.get(order.ticker, Position(order.ticker))
        randomSlippagePercent: float = (1 - random.uniform(0.0, self.slippagePercent))
        unitPrice: float = tickerData.close * randomSlippagePercent

        if position.units == 0 or unitPrice == 0 or order.units < 1:
            order.fillStatus = FillStatus.REJECTED
            self.__rejectOrder__(order)
            return

        unitsToSell: int = min(order.units, position.units)
        sellValue: float = unitPrice * unitsToSell
        commissionCash: float = sellValue * self.commissionPercent
        netCashReceived = sellValue - commissionCash
        self.cash += netCashReceived
        order._portfolioCashImpact = netCashReceived
        position.units -= unitsToSell
        self.__positions__[order.ticker] = position

        order._unitsActuallyTraded = unitsToSell
        order.fillStatus = FillStatus.PARTIALLY_FILLED if unitsToSell < order.units else FillStatus.FILLED

        self.__closeOrder__(order)

    def __executeCloseOrder__(self, tickerData: TickerData, order: Order) -> None:
        '''
        Closes an open position by selling all units.

        :param tickerData: The market data used for order execution.
        :param order: The CloseOrder to execute.
        :return: None
        '''

        position: Position = self.__positions__.get(order.ticker, Position(order.ticker))

        if position.units == 0:
            order.fillStatus = FillStatus.REJECTED
            self.__rejectOrder__(order)
            return

        order.units = position.units
        self.__executeSellOrder__(tickerData, order)
            
    def __executeOrders__(self, tickerData: TickerData) -> None:
        '''
        Executes all open orders relevant to the provided ticker data.

        :param tickerData: The TickerData against which to match and execute orders.
        :return: None
        '''

        for order in self.__openOrders__:
            if order.fillStatus == FillStatus.CANCELLED:
                self.__rejectOrder__(order)

            if order.ticker == tickerData.ticker:
                match order:
                    case BuyOrder(): self.__executeBuyOrder__(tickerData, order)
                    case SellOrder(): self.__executeSellOrder__(tickerData, order)
                    case CloseOrder(): self.__executeCloseOrder__(tickerData, order)