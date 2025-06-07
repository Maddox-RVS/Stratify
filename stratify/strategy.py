from .order import Order, BuyOrder, SellOrder, CloseOrder
from .stats import StatisticsManager
from datetime import datetime
from .stats import trackers
from typing import Union

class Strategy():
    '''
    Base class for defining trading strategies.
    '''

    def __init__(self):
        '''
        Initializes a new strategy instance.
        '''

        self.ticker: Union[None, str] = None
        self.dateTime: Union[None, datetime] = None
        self.open: Union[None, float] = None
        self.close: Union[None, float] = None
        self.low: Union[None, float] = None
        self.high: Union[None, float] = None
        self.volume: Union[None, int] = None

        self.__statisticsManager__: StatisticsManager = StatisticsManager()
        self.__orders__: list[Order] = []
        self.__hasStarted__: bool = False

    def __addDefaultStatisticTrackers__(self):
        # Basic Performance Statistics
        self.__statisticsManager__.addStatisticTracker(trackers.TotalReturnTracker)
        self.__statisticsManager__.addStatisticTracker(trackers.AnnualizedReturnTracker)
        self.__statisticsManager__.addStatisticTracker(trackers.StartingCashTracker)
        self.__statisticsManager__.addStatisticTracker(trackers.FinalPortfolioValueTracker)
        self.__statisticsManager__.addStatisticTracker(trackers.NetProfitOrLossTracker)

        # Drawdown Statistics
        self.__statisticsManager__.addStatisticTracker(trackers.Drawdown)

    def start(self) -> None:
        '''
        Called once before the strategy begins processing data.
        Intended to be overridden by custom strategies.

        :return: None
        '''

        pass

    def next(self) -> None:
        '''
        Called on every new data point (bar). Contains main strategy logic.
        Intended to be overridden by custom strategies.

        :return: None
        '''

        pass

    def end(self) -> None:
        '''
        Called once after all data has been processed.
        Intended to be overridden by custom strategies.

        :return: None
        '''

        pass

    def buy(self, units: int = 1) -> Order:
        '''
        Places a buy order for the current ticker.

        :param units: Number of units to buy.
        :return: The created BuyOrder object.
        '''

        order: BuyOrder = BuyOrder(self.ticker, units)
        self.__orders__.append(order)
        self.__statisticsManager__.strategyOrdersMade.append(order)
        return order

    def sell(self, units: int = 1) -> Order:
        '''
        Places a sell order for the current ticker.

        :param units: Number of units to sell.
        :return: The created SellOrder object.
        '''

        order: SellOrder = SellOrder(self.ticker, units)
        self.__orders__.append(order)
        self.__statisticsManager__.strategyOrdersMade.append(order)
        return order

    def close(self) -> Order:
        '''
        Closes the current position by placing a CloseOrder.

        :return: The created CloseOrder object.
        '''

        order: CloseOrder = CloseOrder(self.ticker)
        self.__orders__.append(order)
        self.__statisticsManager__.strategyOrdersMade.append(order)
        return order
    
    def getStatistic(self, statisticID: str) -> any:
        '''
        Retrieves a statistic by its ID from the strategy's statistics manager.

        :param statisticID: The unique identifier of the statistic to retrieve.
        :return: The value or object associated with the specified statistic ID.
        '''
        
        return self.__statisticsManager__.getStatistic(statisticID)