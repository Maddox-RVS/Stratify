from ..statistic_tracker import StatisticTracker

class FinalPortfolioValueTracker(StatisticTracker):
    def __init__(self):
        super().__init__('final_portfolio_value')

        self.finalValue: float = 0.0

    def end(self) -> None:
        self.finalValue = self.portfolioValue

    def getStats(self) -> float:
        return self.finalValue
    
    def getStatsStr(self) -> str:
        return f'Final Portfolio Value: ${self.finalValue:,.2f}'