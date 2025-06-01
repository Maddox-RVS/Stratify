from order import __Order__, BuyOrder, SellOrder, CloseOrder
from dataclasses import dataclass
from datetime import datetime
from data import TickerData
from data import TickerFeed
from data import Position
from typing import Union

class BrokerStandard():
    def __init__(self):
        self.cash: float = 0.0
        self.commission: float = 0.0

        self.__positions__: dict[str:Position] = {}

        self.__openOrders__: list[__Order__] = []
        self.__closedOrders__: list[__Order__] = []

        self.__dateTime__: Union[None, datetime] = None
        self.__tickerFeeds__: list[TickerFeed] = []

    def setCash(self, cashAmount: float):
        self.cash = cashAmount

    def addCash(self, cashAmount: float):
        self.cash += cashAmount

    def setCommisionPercent(self, commisionPercent: float):
        self.commission = commisionPercent

    def getPosition(self, ticker) -> int:
        tickers: list[str] = [position.ticker for position in self.__positions__]
        if ticker not in tickers: return 0
        for position in self.__positions__:
            if position.ticker == ticker:
                return position.units
            
    def getPortfolioValue(self) -> float:
        value: float = self.cash

        # Creates a tickerfeed containing only ticker data that has a datetime equal to 'dateTime' loop index
        timestampTickerFeed: TickerFeed = TickerFeed([tickerData for tickerFeed in self.__tickerFeeds__ for tickerData in tickerFeed.feed if tickerData.dateTime == self.__dateTime__])
        
        for tickerData in timestampTickerFeed.feed:
            position: Position = self.__positions__.get(tickerData.ticker, Position(tickerData.ticker))
            value += tickerData.close * position.units

        return value
            
    def __executeOrders__(self, tickerData: TickerData):
        for order in self.__openOrders__:
            if order.ticker == tickerData.ticker:
                match order:
                    case BuyOrder(): 
                        orderCost: float = tickerData.close * order.units

                        if self.cash >= orderCost:
                            position: Position = self.__positions__.get(order.ticker, Position(order.ticker))
                            self.cash -= orderCost
                            position.units = order.units
                            self.__positions__[order.ticker] = position

                        self.__closedOrders__.append(order)
                        self.__openOrders__.remove(order)
                    case SellOrder():
                        sellValue: float = tickerData.close * order.units

                        position: Position = self.__positions__.get(order.ticker, Position(order.ticker))
                        if position.units >= order.units:
                            self.cash += sellValue
                            position.units -= order.units
                            self.__positions__[order.ticker] = position

                        self.__closedOrders__.append(order)
                        self.__openOrders__.remove(order)
                    case CloseOrder():
                        position: Position = self.__positions__.get(order.ticker, Position(order.ticker))
                        sellValue: float = tickerData.close * position.units
                        self.cash += sellValue
                        position.units = 0

                        self.__closedOrders__.append(order)
                        self.__openOrders__.remove(order)