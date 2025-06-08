from datetime import timedelta
from typing import Union, Any
from datetime import datetime
from ... import stratify

class MyStrategy(stratify.Strategy):
    '''
    Custom trading strategy implementation.
    '''

    def __init__(self):
        super().__init__()

def test_Strategy():
    # Create an instance of MyStrategy (which inherits from Strategy)
    strategy = MyStrategy()

    # Check if the instance is of type Strategy
    assert isinstance(strategy, stratify.Strategy), 'MyStrategy should be an instance of Strategy'

    # Check defult values of strategy attributes
    assert strategy.ticker is None, 'Default ticker should be None'
    assert strategy.dateTime is None, 'Default dateTime should be None'
    assert strategy.open is None, 'Default open should be None'
    assert strategy.close is None, 'Default close should be None'
    assert strategy.low is None, 'Default low should be None'
    assert strategy.high is None, 'Default high should be None'
    assert strategy.volume is None, 'Default volume should be None'
    assert isinstance(strategy.__statisticsManager__, stratify.stats.StatisticsManager), 'StatisticsManager should be an instance of StatisticsManager'
    assert len(strategy.__orders__) == 0, 'Default orders list should be empty'
    assert not strategy.__hasStarted__, 'Default hasStarted should be False'

    # Check adding default statistics trackers
    strategy.__addDefaultStatisticTrackers__()
    assert len(strategy.__statisticsManager__.__statisticTrackers__) > 0, 'Default statistic trackers should be added'

    # Check creating a buy order
    order: stratify.order.Order = strategy.buy(units=10)
    assert isinstance(order, stratify.order.BuyOrder), 'Order should be an instance of BuyOrder'
    assert order.ticker == None, 'Order ticker should be "None"'
    assert order.units == 10, 'Order units should be 10'
    assert order.fillStatus == stratify.order.FillStatus.PENDING, 'Order status should be PENDING'
    assert len(strategy.__orders__) == 1, 'Orders list should contain 1 order'
    assert order in strategy.__orders__, 'Order should be in the strategy orders list'
    assert order in strategy.__statisticsManager__.strategyOrdersMade, 'Order should be in the statistics manager orders list'

    order: stratify.order.Order = strategy.buy()
    assert isinstance(order, stratify.order.BuyOrder), 'Order should be an instance of BuyOrder'
    assert order.ticker == None, 'Order ticker should be "None"'
    assert order.units == 1, 'Order units should be 1'
    assert order.fillStatus == stratify.order.FillStatus.PENDING, 'Order status should be PENDING'
    assert len(strategy.__orders__) == 2, 'Orders list should contain 2 orders'
    assert order in strategy.__orders__, 'Order should be in the strategy orders list'
    assert order in strategy.__statisticsManager__.strategyOrdersMade, 'Order should be in the statistics manager orders list'
    
    # Check creating a sell order
    order = strategy.sell(units=5)
    assert isinstance(order, stratify.order.SellOrder), 'Order should be an instance of SellOrder'
    assert order.ticker == None, 'Order ticker should be "None"'
    assert order.units == 5, 'Order units should be 5'
    assert order.fillStatus == stratify.order.FillStatus.PENDING, 'Order status should be PENDING'
    assert len(strategy.__orders__) == 3, 'Orders list should contain 3 orders'
    assert order in strategy.__orders__, 'Order should be in the strategy orders list'
    assert order in strategy.__statisticsManager__.strategyOrdersMade, 'Order should be in the statistics manager orders list'

    order = strategy.sell()
    assert isinstance(order, stratify.order.SellOrder), 'Order should be an instance of SellOrder'
    assert order.ticker == None, 'Order ticker should be "None"'
    assert order.units == 1, 'Order units should be 1'
    assert order.fillStatus == stratify.order.FillStatus.PENDING, 'Order status should be PENDING'
    assert len(strategy.__orders__) == 4, 'Orders list should contain 4 orders'
    assert order in strategy.__orders__, 'Order should be in the strategy orders list'
    assert order in strategy.__statisticsManager__.strategyOrdersMade, 'Order should be in the statistics manager orders list'

    # Check creating a close order
    order = strategy.closePosition()
    assert isinstance(order, stratify.order.CloseOrder), 'Order should be an instance of CloseOrder'
    assert order.ticker == None, 'Order ticker should be "None"'
    assert order.units == 1, 'Order units should be 1'
    assert order.fillStatus == stratify.order.FillStatus.PENDING, 'Order status should be PENDING'
    assert len(strategy.__orders__) == 5, 'Orders list should contain 5 orders'
    assert order in strategy.__orders__, 'Order should be in the strategy orders list'
    assert order in strategy.__statisticsManager__.strategyOrdersMade, 'Order should be in the statistics manager orders list'

    # Check getting statistics from strategy
    totalReturn: float = strategy.getStatistic(stratify.StatID.TOTAL_RETURN)
    assert totalReturn is not None, 'Total Return should not be "None"'
    assert totalReturn == 0.0, 'Total return should be equal to 0.0'

    annualizedReturn: float = strategy.getStatistic(stratify.StatID.ANNUALIZED_RETURN)
    assert annualizedReturn is not None, 'Annualized Return should not be "None"'
    assert annualizedReturn == 0.0, 'Annualized Return should be equal to 0.0'

    startingCash: Union[None, float] = strategy.getStatistic(stratify.StatID.STARTING_CASH)
    assert startingCash is None, 'Starting cash should be "None"'

    finalPortfolioValue: Union[None, float] = strategy.getStatistic(stratify.StatID.FINAL_PORTFOLIO_VALUE)
    assert finalPortfolioValue is None, 'Final portfolio value should be "None"'

    netProfitOrLoss: float = strategy.getStatistic(stratify.StatID.NET_PROFIT_OR_LOSS)
    assert netProfitOrLoss == 0.0, 'Net Profit/Loss should be equal to 0.0'

    drawdown: dict[str, Any] = strategy.getStatistic(stratify.StatID.MAX_DRAWDOWN)
    assert isinstance(drawdown, dict)

    maxDrawdown: float = drawdown['value']
    assert maxDrawdown == 0.0, 'Max Drawdown should be equal to 0.0'

    maxDrawdownPercent: float = drawdown['percent']
    assert maxDrawdownPercent == 0.0, 'Max Drawdown Percent should be equal to 0.0'

    drawdownDuration: timedelta = drawdown['duration']
    assert drawdownDuration == timedelta(), 'Drawdown Duration should be equal to an empty timedelta object'