from .my_test_strategy import MyTestStrategy
from datetime import timedelta
from datetime import datetime
from ... import stratify

tickers: list[str] = ['AAPL', 'META', 'GOOG', 'NVDA', 'MSFT', 'TSLA']

def test_stratify():
    startDate: datetime = datetime(2000, 1, 1)
    endDate: datetime = datetime(2024, 1, 1)

    # Download historical ticker feeds
    tickerFeedList: list[stratify.TickerFeed] = []
    for ticker in tickers:
        tickerFeed: stratify.TickerFeed = stratify.downloadData(ticker, startDate, endDate)
        tickerFeedList.append(tickerFeed)

    # Create backtest engine
    backtestEngine: stratify.BacktestEngine = stratify.BacktestEngine()

    # Add ticker feeds to the backtest engine
    for tickerFeed in tickerFeedList:
        backtestEngine.addTickerFeed(tickerFeed)

    # Add a strategy to the backtest engine
    backtestEngine.addStrategy(MyTestStrategy)

    # Setup broker
    backtestEngine.broker.setCash(10000)
    backtestEngine.broker.setCommissionPercent(0.0)
    backtestEngine.broker.setSlippagePercent(0.0)

    # Assert correct number of strategies
    assert len(backtestEngine.strategies) == 1, 'Expected exactly one strategy to be added to the backtest engine.'

    print(f'\nStarting Portfolio Value: {backtestEngine.broker.getPortfolioValue()}\n')
    assert backtestEngine.broker.getPortfolioValue() == 10000, 'Initial portfolio value should be $10,000.'

    print('Running backtest engine...\n')

    # Run the backtest engine
    backtestEngine.run()

    # Assert that the strategy produced the expected statistical results
    for strategy in backtestEngine.strategies:
        totalReturn: float = strategy.getStatistic(stratify.StatID.TOTAL_RETURN)
        annualizedReturn: float = strategy.getStatistic(stratify.StatID.ANNUALIZED_RETURN)
        startingCash: float = strategy.getStatistic(stratify.StatID.STARTING_CASH)
        finalPortfolioValue: float = strategy.getStatistic(stratify.StatID.FINAL_PORTFOLIO_VALUE)
        netProfitOrLoss: float = strategy.getStatistic(stratify.StatID.NET_PROFIT_OR_LOSS)
        
        maxDrawdown: float = strategy.getStatistic(stratify.StatID.MAX_DRAWDOWN)['value']
        maxDrawdownPercent: float = strategy.getStatistic(stratify.StatID.MAX_DRAWDOWN)['percent']
        maxDrawdownDuration: int = strategy.getStatistic(stratify.StatID.MAX_DRAWDOWN)['duration']

        assert round(totalReturn, 2) == 190.29, 'Total return should be approximately 190.29%.'
        assert round(annualizedReturn, 2) == 4.54, 'Annualized return should be approximately 4.54%.'
        assert startingCash == 10000, 'Starting cash should be $10,000.'
        assert round(finalPortfolioValue, 2) == 29028.93, 'Final portfolio value should be approximately $29,028.93.'
        assert round(netProfitOrLoss, 2) == 19028.93, 'Net profit/loss should be approximately $19,028.93.'

        assert round(maxDrawdown, 2) == 5522.44, 'Maximum drawdown should be approximately $5,522.44.'
        assert round(maxDrawdownPercent, 2) == 19.88, 'Maximum drawdown percent should be approximately 19.88%.'
        assert maxDrawdownDuration == timedelta(days=515), 'Maximum drawdown duration should be approximately 515 days.'

        for statistic in strategy.__statisticsManager__.__statisticTrackers__:
            print(statistic.getStatsStr())