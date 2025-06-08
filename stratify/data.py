from datetime import datetime
from typing import Iterator

class TickerData():
    def __init__(self, ticker: str, dateTime: datetime, open: float, close: float, low: float, high: float, volume: int):
        '''
        Initializes a TickerData object with the provided parameters.

        :param ticker: The stock ticker symbol.
        :param dateTime: The date and time of the market data point.
        :param open: The opening price.
        :param close: The closing price.
        :param low: The lowest price of the bar.
        :param high: The highest price of the bar.
        :param volume: The trading volume.
        '''

        self.ticker = ticker
        self.dateTime = dateTime
        self.open = open
        self.close = close
        self.low = low
        self.high = high
        self.volume = volume

    def __eq__(self, other) -> bool:
        if isinstance(other, TickerData):
            return (self.ticker == other.ticker and
                    self.dateTime == other.dateTime and
                    round(self.open, 3) == round(other.open, 3) and
                    round(self.close, 3) == round(other.close, 3) and
                    round(self.low, 3) == round(other.low, 3) and
                    round(self.high, 3) == round(other.high, 3) and
                    self.volume == other.volume)
        return False
    
    def __str__(self) -> str:
        return (f'TickerData(ticker={self.ticker}, ',
                f'dateTime={self.dateTime.strftime("%Y-%m-%d %H:%M:%S")}, ',
                f'open={self.open:.2f}, close={self.close:.2f}, ',
                f'low={self.low:.2f}, high={self.high:.2f}, ',
                f'volume={self.volume})')
    
    def __repr__(self) -> str:
        return self.__str__()

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
    
    def __str__(self) -> str:
        '''
        Returns a string representation of the TickerFeed.

        :return: A string representation of the TickerFeed.
        '''

        result: str = f'TickerFeed:{{{self.feed[0]} ... {len(self.feed) - 2} others ... {self.feed[-1]}}}'
        if len(self.feed) == 2: result = f'TickerFeed:{{{self.feed[0]}, {self.feed[1]}}}'
        if len(self.feed) == 1: result = f'TickerFeed:{{{self.feed[0]}}}'
        if len(self.feed) == 0: result = 'TickerFeed:{{Empty}}'

        return result
    
    def __repr__(self) -> str:
        '''
        Returns a string representation of the TickerFeed.

        :return: A string representation of the TickerFeed.
        '''

        return self.__str__()
    
    def __eq__(self, other) -> bool:
        '''
        Compares this TickerFeed with another for equality.

        :param other: The other TickerFeed to compare with.
        :return: True if both feeds contain the same TickerData items in the same order, False otherwise.
        '''

        if isinstance(other, TickerFeed):
            for tickerData, tickerDataOther in zip(self.feed, other.feed):
                if tickerData != tickerDataOther:
                    return False
                
            if len(self.feed) != len(other.feed):
                return False
            
            return True
        return False
    
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