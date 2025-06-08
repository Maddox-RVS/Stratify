from ..statistic_tracker import StatisticTracker
from typing import Union

class FinalPortfolioValueTracker(StatisticTracker):
    def __init__(self):
        super().__init__('final_portfolio_value')

        self.finalValue: Union[None, float] = None

    def end(self) -> None:
        self.finalValue = self.portfolioValue

    def getStats(self) -> float:
        return self.finalValue
    
    def getStatsStr(self) -> str:
        return f'Final Portfolio Value: ${self.finalValue:,.2f}'