from dataclasses import dataclass
from datetime import datetime

@dataclass
class TickerData():
    ticker: str
    dateTime: datetime
    open: float
    close: float
    low: float
    high: float
    volume: int

class TickerFeed():
    def __init__(self, data: list[TickerData] = None):
        if data == None: data = []
        self.feed: list[TickerData] = data

    def __len__(self) -> int:
        return len(self.feed)
    
    def getByFirstDate(self) -> datetime:
        allDateTimes: list[datetime] = [tickerData.dateTime for tickerData in self.feed]
        return min(allDateTimes)

    def getByLastDate(self) -> datetime:
        allDateTimes: list[datetime] = [tickerData.dateTime for tickerData in self.feed]
        return max(allDateTimes)
    
@dataclass
class Position:
    ticker: str
    units: int = 0