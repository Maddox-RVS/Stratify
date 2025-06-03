from order import Order, BuyOrder, SellOrder, CloseOrder, FillStatus
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

        self.__openOrders__: list[Order] = []
        self.__closedOrders__: list[Order] = []

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
    
    def __getTickerInfo__(self, ticker: str) -> TickerData:
        # Finds ticker data containing only a datetime equal to 'dateTime' loop index and has a ticker equal to 'ticker' argument
        tickerInfo: TickerData = [tickerData for tickerFeed in self.__tickerFeeds__ for tickerData in tickerFeed.feed 
                                                    if tickerData.dateTime == self.__dateTime__ and tickerData.ticker == ticker][0]
        return tickerInfo
    
    def __closeOrder__(self, order: Order):
        self.__closedOrders__.append(order)
        self.__openOrders__.remove(order)
    def __rejectOrder__(self, order: Order):
        self.__openOrders__.remove(order)

    def __executeBuyOrder__(self, tickerData: TickerData, order: Order):
        tickerVolume: int = tickerData.volume
        unitsNeeded: int = min(order.units, tickerVolume)
        unitPrice: float = tickerData.close

        if unitPrice > self.cash or self.cash == 0.0 or tickerVolume == 0 or order.units < 1:
            order.fillStatus = FillStatus.REJECTED
            self.__rejectOrder__(order)
            return
        
        tangibleUnits: int = min(unitsNeeded, int(self.cash / unitPrice))
        orderCost: float = unitPrice * tangibleUnits

        position: Position = self.__positions__.get(order.ticker, Position(order.ticker))
        self.cash -= orderCost
        position.units += tangibleUnits
        self.__positions__[order.ticker] = position

        order.fillStatus = FillStatus.PARTIALLY_FILLED if tangibleUnits < order.units else FillStatus.FILLED

        self.__closeOrder__(order)

    def __executeSellOrder__(self, tickerData: TickerData, order: Order):
        position: Position = self.__positions__.get(order.ticker, Position(order.ticker))
        unitPrice: float = tickerData.close

        if position.units == 0 or unitPrice == 0 or order.units < 1:
            order.fillStatus = FillStatus.REJECTED
            self.__rejectOrder__(order)
            return

        unitsToSell: int = min(order.units, position.units)
        sellValue: float = unitPrice * unitsToSell
        self.cash += sellValue
        position.units -= unitsToSell
        self.__positions__[order.ticker] = position

        order.fillStatus = FillStatus.PARTIALLY_FILLED if unitsToSell < order.units else FillStatus.FILLED

        self.__closeOrder__(order)

    def __executeCloseOrder__(self, tickerData: TickerData, order: Order):
        position: Position = self.__positions__.get(order.ticker, Position(order.ticker))

        if position.units == 0:
            order.fillStatus = FillStatus.REJECTED
            self.__rejectOrder__(order)
            return

        order.units = position.units
        self.__executeSellOrder__(tickerData, order)
            
    def __executeOrders__(self, tickerData: TickerData):
        for order in self.__openOrders__:
            if order.fillStatus == FillStatus.CANCELLED:
                self.__rejectOrder__(order)

            if order.ticker == tickerData.ticker:
                match order:
                    case BuyOrder(): self.__executeBuyOrder__(tickerData, order)
                    case SellOrder(): self.__executeSellOrder__(tickerData, order)
                    case CloseOrder(): self.__executeCloseOrder__(tickerData, order)