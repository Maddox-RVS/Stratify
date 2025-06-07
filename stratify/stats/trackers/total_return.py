from ..statistic_tracker import StatisticTracker

class TotalReturnTracker(StatisticTracker):
    def __init__(self):
        super().__init__('total_return')

        self.totalReturn: float = 0.0

    def end(self) -> None:
        finalValue: float = self.ssCurrentValue

        self.totalReturn = ((finalValue - self.startingCash) / self.startingCash) * 100.0

    def getStats(self) -> float:
        return self.totalReturn
    
    def getStatsStr(self) -> str:
        return f'Total Return: {round(self.totalReturn, 2)}%'