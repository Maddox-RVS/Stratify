from .. import stratify

class MyTestStrategy(stratify.Strategy):
    def __init__(self):
        super().__init__()

        self.bought: bool = False

    def next(self):
        if not self.bought: self.buy(100)
        self.bought = True