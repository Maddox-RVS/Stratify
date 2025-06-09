from .my_test_strategies import MyTestStrategy_BuyAndHold, MyTestStrategy_Random
from datetime import timedelta
from datetime import datetime
from .. import stratify
from typing import Any
import math

tickers: list[str] = ['AAPL', 'META', 'GOOG', 'NVDA', 'MSFT', 'TSLA']

def test_stratify():
    startDate: datetime = datetime(2024, 1, 1)
    endDate: datetime = datetime(2024, 5, 1)

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
    backtestEngine.addStrategy(MyTestStrategy_BuyAndHold)
    backtestEngine.addStrategy(MyTestStrategy_Random)

    # Setup broker
    backtestEngine.broker.setCash(10000)
    backtestEngine.broker.setCommissionPercent(0.0)
    backtestEngine.broker.setSlippagePercent(0.0)

    # Assert correct number of strategies
    assert len(backtestEngine.strategies) == 2, 'Expected exactly 2 strategies to be added to the backtest engine.'

    print(f'\nStarting Portfolio Value: {backtestEngine.broker.getPortfolioValue()}\n')
    assert backtestEngine.broker.getPortfolioValue() == 10000, 'Initial portfolio value should be $10,000.'

    print('Running backtest engine...\n')

    # Run the backtest engine
    backtestEngine.run()

    # Assert that the strategy produced the expected statistical results
    for strategy in backtestEngine.strategies:
        print('---------------------------------------------')
        for statistic in strategy._statisticsManager._statisticTrackers:
            print(statistic.getStatsStr())
    print('---------------------------------------------')

    strategy: stratify.Strategy = backtestEngine.strategies[0]
    totalReturn: float = strategy.getStatistic(stratify.StatID.TOTAL_RETURN)
    annualizedReturn: float = strategy.getStatistic(stratify.StatID.ANNUALIZED_RETURN)
    startingCash: float = strategy.getStatistic(stratify.StatID.STARTING_CASH)
    finalPortfolioValue: float = strategy.getStatistic(stratify.StatID.FINAL_PORTFOLIO_VALUE)
    netProfitOrLoss: float = strategy.getStatistic(stratify.StatID.NET_PROFIT_OR_LOSS)
    
    drawdown: dict[str, Any] = strategy.getStatistic(stratify.StatID.MAX_DRAWDOWN)
    maxDrawdown: float = drawdown['value']
    maxDrawdownPercent: float = drawdown['percent']
    maxDrawdownDuration: int = drawdown['duration']

    trades: dict[str, Any] = strategy.getStatistic(stratify.StatID.TRADES)
    totalTrades: int = trades['total']
    wonTrades: int = trades['won']
    lostTrades: int = trades['lost']
    tradesWinRate: float = trades['win_rate']
    avgProfitPerTrade: float = trades['avg_profit_per_trade']
    largestWinTrade: float = trades['largest_win']
    largestLossTrade: float = trades['largest_loss']
    avgTradeHoldingPeriod: timedelta = trades['avg_holding_period']

    assert math.isclose(round(totalReturn, 2), -8.09, abs_tol=0.01) == True, 'Total return should be approximately -8.09%.'
    assert math.isclose(round(annualizedReturn, 2) , -22.81, abs_tol=0.01) == True, 'Annualized return should be approximately -22.81%.'
    assert startingCash == 10000, 'Starting cash should be $10,000.'
    assert math.isclose(round(finalPortfolioValue, 2), 11197.41, abs_tol=0.01) == True, 'Final portfolio value should be approximately $11,197.41.'
    assert math.isclose(round(netProfitOrLoss, 2), -809.08, abs_tol=0.01) == True, 'Net profit/loss should be approximately $-809.08.'

    assert math.isclose(round(maxDrawdown, 2), 1606.58, abs_tol=0.01) == True, 'Maximum drawdown should be approximately $1,606.58.'
    assert math.isclose(round(maxDrawdownPercent, 2), 15.28, abs_tol=0.01) == True, 'Maximum drawdown percent should be approximately 15.28%.'
    assert maxDrawdownDuration == timedelta(days=98), 'Maximum drawdown duration should be approximately 98 days.'

    assert totalTrades == 0, 'Total trades should be 0.'
    assert wonTrades == 0, 'Total trades won should be 0.'
    assert lostTrades == 0, 'Total trades lost should be 0.'
    assert tradesWinRate == 0, 'The trade win rate should be 0%.'
    assert avgProfitPerTrade == 0, 'The average profit per trade should be $0.'
    assert largestWinTrade == 0, 'The largest win trade should be $0.'
    assert largestLossTrade == 0, 'The largest losing trade should be $0.'
    assert avgTradeHoldingPeriod < timedelta(seconds=0.1), 'The average holding period for a trade should be around 0 seconds.'

    strategy: stratify.Strategy = backtestEngine.strategies[1]
    totalReturn: float = strategy.getStatistic(stratify.StatID.TOTAL_RETURN)
    annualizedReturn: float = strategy.getStatistic(stratify.StatID.ANNUALIZED_RETURN)
    startingCash: float = strategy.getStatistic(stratify.StatID.STARTING_CASH)
    finalPortfolioValue: float = strategy.getStatistic(stratify.StatID.FINAL_PORTFOLIO_VALUE)
    netProfitOrLoss: float = strategy.getStatistic(stratify.StatID.NET_PROFIT_OR_LOSS)
    
    drawdown: dict[str, Any] = strategy.getStatistic(stratify.StatID.MAX_DRAWDOWN)
    maxDrawdown: float = drawdown['value']
    maxDrawdownPercent: float = drawdown['percent']
    maxDrawdownDuration: int = drawdown['duration']

    trades: dict[str, Any] = strategy.getStatistic(stratify.StatID.TRADES)
    totalTrades: int = trades['total']
    wonTrades: int = trades['won']
    lostTrades: int = trades['lost']
    tradesWinRate: float = trades['win_rate']
    avgProfitPerTrade: float = trades['avg_profit_per_trade']
    largestWinTrade: float = trades['largest_win']
    largestLossTrade: float = trades['largest_loss']
    avgTradeHoldingPeriod: timedelta = trades['avg_holding_period']

    assert math.isclose(round(totalReturn, 2), 20.06, abs_tol=0.01) == True, 'Total return should be approximately 20.06%.'
    assert math.isclose(round(annualizedReturn, 2), 75.29, abs_tol=0.01) == True, 'Annualized return should be approximately 75.29%.'
    assert startingCash == 10000, 'Starting cash should be $10,000.'
    assert math.isclose(round(finalPortfolioValue, 2), 11197.41, abs_tol=0.01) == True, 'Final portfolio value should be approximately $11,197.41.'
    assert math.isclose(round(netProfitOrLoss, 2), 2006.49, abs_tol=0.01) == True, 'Net profit/loss should be approximately $2,006.49.'

    assert math.isclose(round(maxDrawdown, 2), 623.27, abs_tol=0.01) == True, 'Maximum drawdown should be approximately $623.27.'
    assert math.isclose(round(maxDrawdownPercent, 2), 5.19, abs_tol=0.01) == True, 'Maximum drawdown percent should be approximately 5.19%.'
    assert maxDrawdownDuration == timedelta(days=18), 'Maximum drawdown duration should be approximately 18 days.'

    assert totalTrades == 109, 'Total trades should be 109.'
    assert wonTrades == 69, 'Total trades won should be 69.'
    assert lostTrades == 40, 'Total trades lost should be 40.'
    assert math.isclose(round(tradesWinRate, 2), 63.3, abs_tol=0.01) == True, 'The trade win rate should be 63.3%.'
    assert math.isclose(round(avgProfitPerTrade, 2), 567.59, abs_tol=0.01) == True, 'The average profit per trade should be $567.59.'
    assert math.isclose(round(largestWinTrade, 2), 7495.54, abs_tol=0.01) == True, 'The largest win trade should be $7495.54.'
    assert math.isclose(round(largestLossTrade, 2), -5960.15, abs_tol=0.01) == True, 'The largest losing trade should be $-5960.15.'
    assert avgTradeHoldingPeriod > timedelta(seconds=1.0), 'The average holding period for a trade should be above 1 second.'