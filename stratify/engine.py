from abc import ABC, abstractmethod
from .stats import StatisticTracker
from .broker import BrokerStandard
from .strategy import Strategy
from datetime import datetime
from .data import TickerData
from .data import TickerFeed
import yfinance
import pandas
import copy

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

class __Engine__(ABC):
    '''
    Abstract base class for a trading engine. Provides an interface for adding ticker data and strategies,
    and running the backtest or live paper trading session.
    '''

    @abstractmethod
    def addTickerFeed(self, tickerFeed: TickerFeed) -> None:
        '''
        Adds a ticker feed to the engine.

        :param tickerData: An object 'TickerFeed' which contains a feed of TickerData objects.
        :return: None
        '''

        pass

    @abstractmethod
    def addStrategy(self, strategy: Strategy) -> None:
        '''
        Adds a trading strategy to the engine.

        :param strategy: A strategy class that inherits from the Strategy base class.
        :return: None
        '''

        pass

    @abstractmethod
    def run(self) -> None:
        '''
        Runs the trading engine, executing each strategy over the given market data.

        :return: None.
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

    def addTickerFeed(self, tickerFeed: TickerFeed) -> None:
        '''
        Adds a ticker feed to the engine and updates the broker with the initial date.

        :param tickerFeed: A TickerFeed object containing historical market data.
        :return: None
        '''

        self.tickerFeeds.append(tickerFeed)
        self.broker._tickerFeeds = self.tickerFeeds
        self.broker._dateTime = self.__getFirstDate__()

    def addStrategy(self, strategyClass: type[Strategy]) -> None:
        '''
        Instantiates and adds a strategy to the engine.

        :param strategy: A subclass of Strategy to be added and instantiated.
        :return: None
        '''

        self.strategies.append(strategyClass())

    def addStatistic(self, statisticTrackerClass: type[StatisticTracker]) -> None:
        '''
        Adds a statistic tracker class to the statistics manager of each strategy.

        :param statisticTrackerClass: A class that inherits from StatisticTracker and will be used to track strategy statistics.
        :return: None
        '''
        
        for strategy in self.strategies:
            strategy._statisticsManager.addStatisticTracker(statisticTrackerClass)

    def run(self) -> None:
        '''
        Runs all added strategies on the historical data in chronological order.
        Simulates order execution using the broker.

        :return: None.
        '''

        for strategy in self.strategies:
            strategy._statisticsManager.setTickerFeeds(self.tickerFeeds)
            strategy.__addDefaultStatisticTrackers__()

        allDateTimes: list[datetime] = []
        for tickerFeed in self.tickerFeeds:
            for tickerData in tickerFeed:
                allDateTimes.append(tickerData.dateTime)
        allDateTimes = sorted(set(allDateTimes))

        for dateTime in allDateTimes:
            self.broker._dateTime = dateTime

            timestampTickerFeed: TickerFeed = TickerFeed()
            for tickerFeed in self.tickerFeeds:
                for tickerData in tickerFeed:
                    if tickerData.dateTime == dateTime:
                        timestampTickerFeed.append(tickerData)

            for tickerData in timestampTickerFeed:
                for strategy in self.strategies:
                    strategy.ticker = tickerData.ticker
                    strategy.dateTime = tickerData.dateTime
                    strategy.open = tickerData.open
                    strategy.close = tickerData.close
                    strategy.low = tickerData.low
                    strategy.high = tickerData.high
                    strategy.volume = tickerData.volume

                    if not strategy._hasStarted:
                        strategy.start()
                        strategy._hasStarted = True

                    strategy.next()

                    self.broker._openOrders += strategy._orders
                    strategy._orders.clear()

                    strategy._statisticsManager.updateStatisticsInfo(strategy.ticker,
                                                                    strategy.dateTime,
                                                                    strategy.open,
                                                                    strategy.close,
                                                                    strategy.low,
                                                                    strategy.high,
                                                                    strategy.volume,
                                                                    self.broker.cash,
                                                                    self.broker.getPortfolioValue(),
                                                                    self.broker.commissionPercent,
                                                                    self.broker.slippagePercent,
                                                                    copy.deepcopy(self.broker._positions),
                                                                    copy.deepcopy(self.broker._openOrders) + copy.deepcopy(self.broker._closedOrders),
                                                                    copy.deepcopy(self.broker._openOrders),
                                                                    copy.deepcopy(self.broker._closedOrders))
                    if not strategy._statisticsManager.hasStarted:
                        strategy._statisticsManager.start()
                        strategy._statisticsManager.hasStarted = True

                    strategy._statisticsManager.update()

                self.broker.__executeOrders__(tickerData)

        for strategy in self.strategies:
            strategy.end()
            strategy._statisticsManager.end()