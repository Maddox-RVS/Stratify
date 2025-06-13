from .. import stratify

class MyTestStrategy_BuyAndHold(stratify.Strategy):
    def __init__(self):
        super().__init__()

        self.bought: bool = False

    def next(self):
        if not self.bought: self.buy(100)
        self.bought = True

class MyTestStrategy_BuyAndSellFlip(stratify.Strategy):
    def __init__(self):
        super().__init__()

        self.flip: int = 0

    def next(self):
        self.flip += 1

        if self.flip < 10:
            self.buy(units=10)
        else: 
            self.sell(units=10)
            if self.flip == 20:
                self.flip = 0