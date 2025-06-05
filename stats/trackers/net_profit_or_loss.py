from ..statistic_tracker import StatisticTracker

class NetProfitOrLossTracker(StatisticTracker):
    def __init__(self):
        super().__init__('net_profit_or_loss')

        self.finalValue: float = 0.0

        self.__initialValue__: float = 0.0

    def start(self) -> None:
        self.__initialValue__ = self.portfolioValue

    def end(self) -> None:
        self.finalValue = self.portfolioValue - self.__initialValue__

    def getStats(self) -> float:
        return self.finalValue
    
    def getStatsStr(self) -> str:
        return f'Net Profit/Loss: ${self.finalValue:,.2f}'