from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

@dataclass
class TickerData():
    '''
    Represents a single bar of market data for a specific ticker and timestamp.

    :param ticker: The stock ticker symbol.
    :param dateTime: The date and time of the market data point.
    :param open: The opening price.
    :param close: The closing price.
    :param low: The lowest price of the bar.
    :param high: The highest price of the bar.
    :param volume: The trading volume.
    '''

    ticker: str
    dateTime: datetime
    open: float
    close: float
    low: float
    high: float
    volume: int

class TickerFeed():
    '''
    A container for storing a list of TickerData objects and accessing them in time order.
    '''

    def __init__(self, data: list[TickerData] = None):
        '''
        Initializes the TickerFeed with optional data.

        :param data: Optional list of TickerData objects. If None, initializes with an empty list.
        '''

        if data == None: data = []
        self.feed: list[TickerData] = data

    def __len__(self) -> int:
        '''
        Returns the number of TickerData items in the feed.

        :return: The number of TickerData items.
        '''

        return len(self.feed)
    
    def __iter__(self) -> Iterator[TickerData]:
        '''
        Returns an iterator over the TickerData items in the feed.

        :return: An iterator of TickerData objects.
        '''

        return iter(self.feed)
    
    def append(self, tickerData: TickerData) -> None:
        '''
        Appends a TickerData object to the feed.

        :param tickerData: The TickerData object to append.
        :return: None
        '''
        
        self.feed.append(tickerData)
    
    def getByFirstDate(self) -> datetime:
        '''
        Returns the earliest date in the TickerFeed.

        :return: The earliest datetime in the feed.
        '''

        allDateTimes: list[datetime] = [tickerData.dateTime for tickerData in self.feed]
        return min(allDateTimes)

    def getByLastDate(self) -> datetime:
        '''
        Returns the latest date in the TickerFeed.

        :return: The latest datetime in the feed.
        '''

        allDateTimes: list[datetime] = [tickerData.dateTime for tickerData in self.feed]
        return max(allDateTimes)
    
@dataclass
class Position:
    '''
    Represents a position held in a specific ticker.

    :param ticker: The stock ticker symbol.
    :param units: The number of units currently held. Defaults to 0.
    '''

    ticker: str
    units: int = 0