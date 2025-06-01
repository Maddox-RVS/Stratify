from strategy import Strategy
from datetime import datetime
from broker import BrokerStandard
from data import TickerData
from data import TickerFeed
import yfinance
import pandas

import mystrat

def downloadData(ticker: str, start: datetime, end: datetime) -> TickerFeed:
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
    def addTickerData(self, data: list[TickerData]):
        pass

    def addStrategy(self, strategy: Strategy):
        pass

    def run(self) -> list[Strategy]:
        pass

class BacktestEngine(__Engine__):
    def __init__(self):
        super().__init__()
        self.tickerFeeds: list[TickerFeed] = []
        self.strategies: list[Strategy] = []
        self.broker: BrokerStandard = BrokerStandard()

    def addTickerData(self, tickerFeed: TickerFeed):
        self.tickerFeeds.append(tickerFeed)

    def addStrategy(self, strategy: Strategy):
        self.strategies.append(strategy())

    def run(self) -> list[Strategy]:
        for strategy in self.strategies: strategy.start()

        allDateTimes: set[datetime] = set([tickerData.dateTime for tickerFeed in self.tickerFeeds for tickerData in tickerFeed.feed])
        for dateTime in allDateTimes:
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

                    self.broker.openOrders += strategy.orders
                    strategy.orders.clear()

                self.broker.__executeOrders__(tickerData)

        for strategy in self.strategies: strategy.end()

        print(f'Open Orders: {len(self.broker.openOrders)}')
        print(f'Closed Orders: {len(self.broker.closedOrders)}')
        print(f'Final Cash Amount: {self.broker.cash}')

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

    backtestEngine.run()