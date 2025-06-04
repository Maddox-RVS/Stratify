from strategy import Strategy
from datetime import datetime
from broker import BrokerStandard
from data import TickerData
from data import TickerFeed
import yfinance
import pandas

import mystrat

def downloadData(ticker: str, start: datetime, end: datetime) -> TickerFeed:
    '''
    Downloads historical stock data for a given ticker between start and end dates using yfinance,
    and converts it into a TickerFeed object.

    :param ticker: The stock ticker symbol (e.g., 'AAPL').
    :param start: The start date of the data range.
    :param end: The end date of the data range.
    :return: A TickerFeed containing TickerData for each trading day in the given range.
    '''
    
    yfinanceData: pandas.DataFrame = yfinance.download(ticker, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), progress=True, auto_adjust=True)
    data: list[TickerData] = []

    for date in yfinanceData.index:
        open: float = float(yfinanceData.loc[date, ('Open', ticker)])
        close: float = float(yfinanceData.loc[date, ('Close', ticker)])
        low: float = float(yfinanceData.loc[date, ('Low', ticker)])
        high: float = float(yfinanceData.loc[date, ('High', ticker)])
        volume: int = int(yfinanceData.loc[date, ('Volume', ticker)])
        tickerData: TickerData = TickerData(ticker, date, open, close, low, high, volume)
        data.append(tickerData)

    return TickerFeed(data)

class __Engine__():
    '''
    Abstract base class for a trading engine. Provides an interface for adding ticker data and strategies,
    and running the backtest or live paper trading session.
    '''

    def addTickerData(self, tickerFeed: TickerFeed) -> None:
        '''
        Adds a ticker feed to the engine.

        :param tickerData: An object 'TickerFeed' which contains a feed of TickerData objects.
        :return: None
        '''

        pass

    def addStrategy(self, strategy: Strategy) -> None:
        '''
        Adds a trading strategy to the engine.

        :param strategy: A strategy class that inherits from the Strategy base class.
        :return: None
        '''

        pass

    def run(self) -> list[Strategy]:
        '''
        Runs the trading engine, executing each strategy over the given market data.

        :return: A list of strategies after execution.
        '''

        pass

class BacktestEngine(__Engine__):
    '''
    Backtesting engine that simulates historical trading using strategies and historical ticker data.
    '''

    def __init__(self):
        '''
        Initializes the BacktestEngine with an empty list of ticker feeds and strategies,
        and a standard broker.
        '''

        super().__init__()
        self.tickerFeeds: list[TickerFeed] = []
        self.strategies: list[Strategy] = []
        self.broker: BrokerStandard = BrokerStandard()

    def __getFirstDate__(self) -> datetime:
        '''
        Gets the earliest date from all ticker feeds.

        :return: The earliest datetime from the ticker data.
        '''

        allFirstDates: list[datetime] = [tickerFeed.getByFirstDate() for tickerFeed in self.tickerFeeds]
        return min(allFirstDates)

    def __getLastDate__(self) -> datetime:
        '''
        Gets the latest date from all ticker feeds.

        :return: The latest datetime from the ticker data.
        '''

        allLastDates: list[datetime] = [tickerFeed.getByLastDate() for tickerFeed in self.tickerFeeds]
        return max(allLastDates)

    def addTickerData(self, tickerFeed: TickerFeed) -> None:
        '''
        Adds a ticker feed to the engine and updates the broker with the initial date.

        :param tickerFeed: A TickerFeed object containing historical market data.
        :return: None
        '''

        self.tickerFeeds.append(tickerFeed)
        self.broker.__tickerFeeds__ = self.tickerFeeds
        self.broker.__dateTime__ = self.__getFirstDate__()

    def addStrategy(self, strategy: Strategy) -> None:
        '''
        Instantiates and adds a strategy to the engine.

        :param strategy: A subclass of Strategy to be added and instantiated.
        :return: None
        '''

        self.strategies.append(strategy())

    def run(self) -> list[Strategy]:
        '''
        Runs all added strategies on the historical data in chronological order.
        Simulates order execution using the broker.

        :return: A list of all strategies after completing the backtest.
        '''

        for strategy in self.strategies: strategy.start()

        # Flattens all datetimes from all tickerfeeds into single list, then removes duplicates and sorts from smallest to largest
        allDateTimes: set[datetime] = sorted(list(set([tickerData.dateTime for tickerFeed in self.tickerFeeds for tickerData in tickerFeed.feed])))

        for dateTime in allDateTimes:
            self.broker.__dateTime__ = dateTime

            # Creates a tickerfeed containing only ticker data that has a datetime equal to 'dateTime' loop index
            timestampTickerFeed: TickerFeed = TickerFeed([tickerData for tickerFeed in self.tickerFeeds for tickerData in tickerFeed.feed if tickerData.dateTime == dateTime])

            for tickerData in timestampTickerFeed.feed:
                for strategy in self.strategies:
                    strategy.ticker = tickerData.ticker
                    strategy.dateTime = tickerData.dateTime
                    strategy.open = tickerData.open
                    strategy.close = tickerData.close
                    strategy.low = tickerData.low
                    strategy.high = tickerData.high
                    strategy.volume = tickerData.volume
                    strategy.next()

                    self.broker.__openOrders__ += strategy.orders
                    strategy.orders.clear()

                self.broker.__executeOrders__(tickerData)

        for strategy in self.strategies: strategy.end()

if __name__ == '__main__':
    data = []
    data.append(downloadData('AAPL', datetime(2000, 1, 1), datetime(2024, 1, 1)))
    data.append(downloadData('META', datetime(2000, 1, 1), datetime(2024, 1, 1)))
    data.append(downloadData('GOOG', datetime(2000, 1, 1), datetime(2024, 1, 1)))
    data.append(downloadData('NVDA', datetime(2000, 1, 1), datetime(2024, 1, 1)))
    data.append(downloadData('MSFT', datetime(2000, 1, 1), datetime(2024, 1, 1)))
    data.append(downloadData('TSLA', datetime(2000, 1, 1), datetime(2024, 1, 1)))

    backtestEngine = BacktestEngine()

    for d in data:
        backtestEngine.addTickerData(d)
    
    backtestEngine.addStrategy(mystrat.MyStrategy)
    
    backtestEngine.broker.setCash(10000)

    print(f'Starting Portfolio Value: {backtestEngine.broker.getPortfolioValue()}')
    
    backtestEngine.run()
    
    print(f'Open Orders: {len(backtestEngine.broker.__openOrders__)}')
    print(f'Closed Orders: {len(backtestEngine.broker.__closedOrders__)}')
    print(f'Final Portfolio Value: {backtestEngine.broker.getPortfolioValue()}')