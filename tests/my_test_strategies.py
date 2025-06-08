from .. import stratify
import random

random.seed(1)

class MyTestStrategy_BuyAndHold(stratify.Strategy):
    def __init__(self):
        super().__init__()

        self.bought: bool = False

    def next(self):
        if not self.bought: self.buy(100)
        self.bought = True

class MyTestStrategy_Random(stratify.Strategy):
    def __init__(self):
        super().__init__()

    def next(self):
        buyOrSell: int = random.randint(0, 1)
        if buyOrSell == 0:
            self.buy(units=20)
        else:
            self.sell(units=20)