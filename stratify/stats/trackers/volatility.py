from ..statistic_tracker import StatisticTracker
import numpy as np

class VolatilityTracker(StatisticTracker):
    def __init__(self):
        super().__init__('volatility')

        self.volatilityPercent: float = 0.0

        self._returns: list[float] = []
        self._portfolioValues: list[float] = []

    def update(self) -> None:
        self._portfolioValues.append(self.ssCurrentValue)

    def end(self) -> None:
        for i in range(1, len(self._portfolioValues)):
            currentValue: float = self._portfolioValues[i]
            previousValue: float = self._portfolioValues[i - 1]
            currentReturn: float = (currentValue - previousValue) / previousValue if previousValue != 0 else 0.0
            self._returns.append(currentReturn)

        self.volatilityPercent = float(np.std(np.array(self._returns), ddof=1)) * 100.0 if len(self._returns) > 1 else 0.0

    def getStats(self) -> float:
        return self.volatilityPercent
    
    def getStatsStr(self) -> str:
        return f'Volatility: {self.volatilityPercent:.2f}%'