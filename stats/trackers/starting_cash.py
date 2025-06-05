from ..statistic_tracker import StatisticTracker

class StartingCashTracker(StatisticTracker):
    def __init__(self):
        super().__init__('starting_cash')

        self.initialCash: float = 0.0

    def start(self) -> None:
        self.initialCash = self.portfolioCash

    def getStats(self) -> float:
        return self.initialCash
    
    def getStatsStr(self) -> str:
        return f'Starting Cash: ${self.initialCash:,.2f}'