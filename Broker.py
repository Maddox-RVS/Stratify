from order import __Order__, BuyOrder, SellOrder, CloseOrder
from dataclasses import dataclass
from data import TickerData
from data import Position

class BrokerStandard():
    def __init__(self):
        self.cash: float = 0.0
        self.commission: float = 0.0

        self.positions: dict[str:Position] = {}

        self.openOrders: list[__Order__] = []
        self.closedOrders: list[__Order__] = []

    def setCash(self, cashAmount: float):
        self.cash = cashAmount

    def addCash(self, cashAmount: float):
        self.cash += cashAmount

    def setCommisionPercent(self, commisionPercent: float):
        self.commission = commisionPercent

    def getPosition(self, ticker) -> int:
        tickers: list[str] = [position.ticker for position in self.positions]
        if ticker not in tickers: return 0
        for position in self.positions:
            if position.ticker == ticker:
                return position.units
            
    def __executeOrders__(self, tickerData: TickerData):
        for order in self.openOrders:
            if order.ticker == tickerData.ticker:
                match order:
                    case BuyOrder(): 
                        orderCost: float = tickerData.close * order.units

                        if self.cash >= orderCost:
                            position: Position = self.positions.get(order.ticker, Position(order.ticker))
                            self.cash -= orderCost
                            position.units = order.units
                            self.positions[order.ticker] = position

                        self.closedOrders.append(order)
                        self.openOrders.remove(order)
                    case SellOrder():
                        sellValue: float = tickerData.close * order.units

                        position: Position = self.positions.get(order.ticker, Position(order.ticker))
                        if position.units >= order.units:
                            self.cash += sellValue
                            position.units -= order.units
                            self.positions[order.ticker] = position

                        self.closedOrders.append(order)
                        self.openOrders.remove(order)
                    case CloseOrder():
                        position: Position = self.positions.get(order.ticker, Position(order.ticker))
                        sellValue: float = tickerData.close * position.units
                        self.cash += sellValue
                        position.units = 0

                        self.closedOrders.append(order)
                        self.openOrders.remove(order)