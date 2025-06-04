from ..statistic_tracker import StatisticTracker

class TotalReturnTracker(StatisticTracker):
    def __init__(self):
        super().__init__('total_return')

        self.totalReturns: float = 0.0

        self.__initialValue__: float = 0.0

    def start(self) -> None:
        self.initialValue = self.portfolioValue

    def end(self) -> None:
        self.totalReturns = self.portfolioValue - self.initialValue

    def getStats(self) -> float:
        return self.totalReturns