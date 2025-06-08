from ...order import Order, FillStatus, BuyOrder, SellOrder, CloseOrder
from ..statistic_tracker import StatisticTracker
from datetime import timedelta
from collections import deque
from typing import Union
from typing import Any

class TradesTracker(StatisticTracker):
    HOURS_IN_DAY: int = 24
    MINS_IN_HOUR: int = 60
    SECS_IN_MIN: int = 60
    SECS_IN_DAY: int = SECS_IN_MIN * MINS_IN_HOUR * HOURS_IN_DAY
    SECS_IN_HOUR: int = SECS_IN_MIN * MINS_IN_HOUR

    EPSILON: float = 1e-8

    def __init__(self):
        super().__init__('trades')

        self.totalTrades: int = 0
        self.wonTrades: int = 0
        self.lostTrades: int = 0
        self.winRate: float = 0.0
        self.averageProfitPerTrade: float = 0.0
        self.largestWin: float = 0.0
        self.largestLoss: float = 0.0
        self.averageTradeHoldingPeriod: timedelta = timedelta()

    def end(self) -> None:
        closedStrategyOrders: list[Order] = []
        for order in self.strategyOrdersMade:
            if order.fillStatus in (FillStatus.FILLED, FillStatus.PARTIALLY_FILLED):
                closedStrategyOrders.append(order)

        tradeProfits: list[float] = []
        totalHoldingTimeSeconds: float = 0.0

        # Calculate won/lost trades
        buyOrders: deque = deque()
        sellOrders: deque = deque()

        for order in closedStrategyOrders:
            if isinstance(order, BuyOrder): buyOrders.append(order)
            elif isinstance(order, (SellOrder, CloseOrder)): sellOrders.append(order)

        while sellOrders and buyOrders:
            sellOrder: Union[SellOrder, CloseOrder] = sellOrders.popleft()
            matchingBuyOrder: BuyOrder = buyOrders.popleft()

            matchedUnits: int  = min(sellOrder.units, matchingBuyOrder.units)

            cashImpactPerSellUnit: float = sellOrder._portfolioCashImpact / sellOrder.units
            cashImpactPerBuyUnit: float = matchingBuyOrder._portfolioCashImpact / matchingBuyOrder.units

            cashImpactSellOrder: float = matchedUnits * cashImpactPerSellUnit
            cashImpactBuyOrder: float = matchedUnits * cashImpactPerBuyUnit

            self.totalTrades += 1

            tradeProfit: float = cashImpactSellOrder + cashImpactBuyOrder
            if tradeProfit > TradesTracker.EPSILON: self.wonTrades += 1
            else: self.lostTrades += 1
            tradeProfits.append(tradeProfit)

            totalHoldingTimeSeconds += (sellOrder.__closedEndTime__ - matchingBuyOrder.__openedStartTime__).total_seconds()

            sellOrder.units -= matchedUnits
            matchingBuyOrder.units -= matchedUnits

            if sellOrder.units != 0:
                sellOrder._portfolioCashImpact = sellOrder.units * cashImpactPerSellUnit
                sellOrders.appendleft(sellOrder)
            if matchingBuyOrder.units != 0:
                matchingBuyOrder._portfolioCashImpact = matchingBuyOrder.units * cashImpactPerBuyUnit
                buyOrders.appendleft(matchingBuyOrder)

        # Calculate final win rate
        self.winRate = (self.wonTrades / self.totalTrades if self.totalTrades != 0 else 0.0) * 100.0

        # Calculate average profit per trade
        self.averageProfitPerTrade = sum(tradeProfits) / len(tradeProfits) if tradeProfits else 0.0

        # Calculate largest win and loss
        self.largestWin = max(tradeProfits) if tradeProfits else 0.0
        self.largestLoss = min(tradeProfits) if tradeProfits else 0.0

        # Calculate average holding time
        averageHoldingTimeSeconds: float = totalHoldingTimeSeconds / self.totalTrades if self.totalTrades != 0 else 0.0
        self.averageTradeHoldingPeriod = timedelta(seconds=averageHoldingTimeSeconds)

    def getStats(self) -> dict[str:Any]:
        return {
            'total': self.totalTrades,
            'won': self.wonTrades,
            'lost': self.lostTrades,
            'win_rate': self.winRate,
            'avg_profit_per_trade': self.averageProfitPerTrade,
            'largest_win': self.largestWin,
            'largest_loss': self.largestLoss,
            'avg_holding_period': self.averageTradeHoldingPeriod}
    
    def getStatsStr(self) -> str:
        totalSeconds: float = self.averageTradeHoldingPeriod.total_seconds()

        days: int = self.averageTradeHoldingPeriod.days
        totalSeconds -= days * TradesTracker.SECS_IN_DAY

        hours: int = int(totalSeconds // TradesTracker.SECS_IN_HOUR)
        totalSeconds -= hours * TradesTracker.SECS_IN_HOUR

        minutes: int = int(totalSeconds // TradesTracker.SECS_IN_MIN)
        totalSeconds -=  minutes * TradesTracker.SECS_IN_MIN

        seconds: float = round(totalSeconds, 3)

        return (f'Trade Statistics:\n'
                f'   Total Trades: {self.totalTrades:,}\n'
                f'      Won Trades: {self.wonTrades:,}\n'
                f'      Lost Trades: {self.lostTrades:,}\n'
                f'      Largest Win: ${round(self.largestWin, 2):,.2f}\n'
                f'      Largest Loss: ${round(self.largestLoss, 2):,.2f}\n'
                f'   Win Rate: {round(self.winRate, 2)}%\n'
                f'   Average Profit Per Trade: ${round(self.averageProfitPerTrade, 2):,.2f}\n'
                f'   Average Holding Period: {days:,} Days, {hours:,} Hours, {minutes:,} Minutes, {seconds:,} Seconds')