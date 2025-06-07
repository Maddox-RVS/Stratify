from ..statistic_tracker import StatisticTracker

class StartingCashTracker(StatisticTracker):
    def __init__(self):
        super().__init__('starting_cash')

    def getStats(self) -> float:
        return self.startingCash
    
    def getStatsStr(self) -> str:
        return f'Starting Cash: ${self.startingCash:,.2f}'