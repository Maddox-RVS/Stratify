from ..statistic_tracker import StatisticTracker

class TotalReturnTracker(StatisticTracker):
    def __init__(self):
        super().__init__('total_return')

        self.totalReturn: float = 0.0

        self.__initialValue__: float = 0.0

    def start(self) -> None:
        self.__initialValue__ = self.portfolioValue

    def end(self) -> None:
        self.totalReturn = ((self.portfolioValue - self.__initialValue__) / self.__initialValue__) * 100.0

    def getStats(self) -> float:
        return self.totalReturn
    
    def getStatsStr(self) -> str:
        return f'Total Return: {round(self.totalReturn, 2)}%'