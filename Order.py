class __Order__():
    def __init__(self, ticker: str, units: int):
        self.ticker: str = ticker
        self.units: int = units

class BuyOrder(__Order__):
    def __init__(self, ticker: str, units: int = 1):
        super().__init__(ticker, units)

class SellOrder(__Order__):
    def __init__(self, ticker: str, units: int = 1):
        super().__init__(ticker, units)

class CloseOrder(__Order__):
    def __init__(self, ticker, units: int = 1):
        super().__init__(ticker, units)