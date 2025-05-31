from dataclasses import dataclass

@dataclass
class Position:
    ticker: str
    units: int

class Broker():
    def __init__(self):
        self.cash: float = 0.0
        self.commission: float = 0.0
        self.positions: list[Position]

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
            
    