from Strategy import Strategy

class MyStrategy(Strategy):
    def __init__(self):
        super().__init__()

    def next(self):
        if self.close > 120.0: self.buy()
        else: self.sell()

    def end(self):
        print(f'{self.__class__.__name__}: {len(self.orders)}')