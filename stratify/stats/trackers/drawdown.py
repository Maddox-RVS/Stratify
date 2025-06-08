from ..statistic_tracker import StatisticTracker
from datetime import timedelta
from datetime import datetime
from typing import Union
import os

class DrawdownTracker(StatisticTracker):
    HOURS_IN_DAY: int = 24
    MINS_IN_HOUR: int = 60
    SECS_IN_MIN: int = 60
    SECS_IN_DAY: int = SECS_IN_MIN * MINS_IN_HOUR * HOURS_IN_DAY
    SECS_IN_HOUR: int = SECS_IN_MIN * MINS_IN_HOUR

    def __init__(self):
        super().__init__('max_drawdown')

        self.maxDrawdownValue: float = 0.0
        self.maxDrawdownPercent: float = 0.0
        self.drawdownDuration: timedelta = timedelta()

        self.__portfolioValues__: list[float] = []
        self.__drawdowns__: list[tuple[float, float, timedelta]] = []

        self.__peak__: float = 0.0
        self.__peakIndex__: Union[None, int] = None
        self.__drawdownStartTime__: Union[None, datetime] = None

    def start(self) -> None:
        self.__peak__ = self.startingValue
        self.__peakIndex__ = 0
        self.__drawdownStartTime__ = self.dateTime

    def __calculateDrawdown__(self, drawdownIndexOffest: int = 2) -> None:
        drawdownEndTime: datetime = self.dateTime
        drawdownDuration: timedelta = drawdownEndTime - self.__drawdownStartTime__

        drawdownEndIndex: int = len(self.__portfolioValues__) - drawdownIndexOffest
        drawdownPeriodValues: list[float] = self.__portfolioValues__[self.__peakIndex__:drawdownEndIndex + 1]
        trough: float = min(drawdownPeriodValues)

        peak: float = drawdownPeriodValues[0]

        drawdownValue: float = peak - trough
        drawdownPercent: float = ((peak - trough) / peak) * 100

        if drawdownValue > 0 and drawdownDuration > timedelta():
            self.__drawdowns__.append((drawdownValue, drawdownPercent, drawdownDuration))

    def update(self) -> None:
        self.__portfolioValues__.append(self.ssCurrentValue)

        if self.ssCurrentValue > self.__peak__:
            self.__calculateDrawdown__()

            self.__peak__ = self.ssCurrentValue
            self.__peakIndex__ = len(self.__portfolioValues__) - 1
            self.__drawdownStartTime__ = self.dateTime

    def end(self) -> None:
        if self.ssCurrentValue < self.__peak__:
            self.__calculateDrawdown__(drawdownIndexOffest=1)

        drawdownValues: list[float] = [drawdown[0] for drawdown in self.__drawdowns__]
        drawdownPercents: list[float] = [drawdown[1] for drawdown in self.__drawdowns__]
        drawdownDurations: list[timedelta] = [drawdown[2] for drawdown in self.__drawdowns__]

        if self.__drawdowns__:
            self.maxDrawdownValue = max(drawdownValues)
            self.maxDrawdownPercent = max(drawdownPercents)
            self.drawdownDuration = drawdownDurations[drawdownValues.index(self.maxDrawdownValue)]

    def getStats(self) -> dict[str:any]:
        return {'value': self.maxDrawdownValue, 'percent': self.maxDrawdownPercent, 'duration': self.drawdownDuration}

    def getStatsStr(self) -> str:
        totalSeconds: float = self.drawdownDuration.total_seconds()

        days: int = self.drawdownDuration.days
        totalSeconds -= days * DrawdownTracker.SECS_IN_DAY

        hours: int = int(totalSeconds // DrawdownTracker.SECS_IN_HOUR)
        totalSeconds -= hours * DrawdownTracker.SECS_IN_HOUR

        minutes: int = int(totalSeconds // DrawdownTracker.SECS_IN_MIN)
        totalSeconds -=  minutes * DrawdownTracker.SECS_IN_MIN

        seconds: float = round(totalSeconds, 3)

        return (f'Drawdown Statistics:\n'
                f'   Max Drawdown: ${round(self.maxDrawdownValue, 2):,.2f}\n'
                f'   Max Drawdown Percent: {round(self.maxDrawdownPercent, 2)}%\n'
                f'   Drawdown Duration: {days:,} Days, {hours:,} Hours, {minutes:,} Minutes, {seconds:,} Seconds')