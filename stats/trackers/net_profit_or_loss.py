from ..statistic_tracker import StatisticTracker

class NetProfitOrLossTracker(StatisticTracker):
    def __init__(self):
        super().__init__('net_profit_or_loss')

    def getStats(self) -> float:
        return self.ssNetValueProfitOrLoss
    
    def getStatsStr(self) -> str:
        return f'Net Profit/Loss: ${self.ssNetValueProfitOrLoss:,.2f}'