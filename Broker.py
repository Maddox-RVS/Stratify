from order import Order, BuyOrder, SellOrder, CloseOrder, FillStatus
from dataclasses import dataclass
from datetime import datetime
from data import TickerData
from data import TickerFeed
from data import Position
from typing import Union

class BrokerStandard():
    '''
    A basic broker model that handles positions, orders, and cash management.
    '''

    def __init__(self):
        '''
        Initializes the broker with default values for cash, commission, positions, and orders.
        '''

        self.cash: float = 0.0
        self.commissionPercent: float = 0.0

        self.__positions__: dict[str:Position] = {}

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

    def setCommisionPercent(self, commisionPercent: float) -> None:
        '''
        Sets the commission percentage charged per trade.

        :param commisionPercent: Commission as a decimal (e.g., 0.01 for 1%).
        :return: None
        '''

        self.commissionPercent = commisionPercent

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

        # Creates a tickerfeed containing only ticker data that has a datetime equal to 'dateTime' loop index
        timestampTickerFeed: TickerFeed = TickerFeed([tickerData for tickerFeed in self.__tickerFeeds__ for tickerData in tickerFeed.feed if tickerData.dateTime == self.__dateTime__])
        
        for tickerData in timestampTickerFeed.feed:
            position: Position = self.__positions__.get(tickerData.ticker, Position(tickerData.ticker))
            value += tickerData.close * position.units

        return value
    
    def __getTickerInfo__(self, ticker: str) -> TickerData:
        '''
        Retrieves TickerData for the given ticker at the current broker datetime.

        :param ticker: The stock ticker symbol.
        :return: The matching TickerData object.
        '''

        # Finds ticker data containing only a datetime equal to 'dateTime' loop index and has a ticker equal to 'ticker' argument
        tickerInfo: TickerData = [tickerData for tickerFeed in self.__tickerFeeds__ for tickerData in tickerFeed.feed 
                                                    if tickerData.dateTime == self.__dateTime__ and tickerData.ticker == ticker][0]
        return tickerInfo
    
    def __closeOrder__(self, order: Order) -> None:
        '''
        Moves an order from open to closed.

        :param order: The order to close.
        :return: None
        '''

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
        unitPrice: float = tickerData.close


        if (unitPrice + (unitPrice * self.commissionPercent)) > self.cash or self.cash <= 0.0 or tickerVolume < 1 or order.units < 1:
            order.fillStatus = FillStatus.REJECTED
            self.__rejectOrder__(order)
            return
        
        tangibleUnits: int = min(unitsNeeded, int(self.cash / (unitPrice + (unitPrice * self.commissionPercent))))
        orderCost: float = unitPrice * tangibleUnits
        commisionCash: float = orderCost * self.commissionPercent

        position: Position = self.__positions__.get(order.ticker, Position(order.ticker))
        self.cash -= (orderCost + commisionCash)
        position.units += tangibleUnits
        self.__positions__[order.ticker] = position

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
        unitPrice: float = tickerData.close

        if position.units == 0 or unitPrice == 0 or order.units < 1:
            order.fillStatus = FillStatus.REJECTED
            self.__rejectOrder__(order)
            return

        unitsToSell: int = min(order.units, position.units)
        sellValue: float = unitPrice * unitsToSell
        commissionCash: float = sellValue * self.commissionPercent
        netCashReceived = sellValue - commissionCash
        self.cash += netCashReceived
        position.units -= unitsToSell
        self.__positions__[order.ticker] = position

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