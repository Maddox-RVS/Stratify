class Order():
    def __init__(self, ticker: str, units: int):
        self.ticker: str = ticker
        self.units: int = units

class BuyOrder(Order):
    def __init__(self, ticker: str, units: int = 1):
        super().__init__(ticker, units)

class SellOrder(Order):
    def __init__(self, ticker: str, units: int = 1):
        super().__init__(ticker, units)