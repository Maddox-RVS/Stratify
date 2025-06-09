

class StatID():
    '''
    Defines constant identifiers for default statistics.

    These IDs can be used to access specific default statistics from the statistics manager.
    '''

    # Basic Performance Statistics
    TOTAL_RETURN: str = 'total_return'
    ANNUALIZED_RETURN: str = 'annualized_return'
    STARTING_CASH: str = 'starting_cash'
    FINAL_PORTFOLIO_VALUE: str = 'final_portfolio_value'
    NET_PROFIT_OR_LOSS: str = 'net_profit_or_loss'
    VOLATILITY: str = 'volatility'

    # Drawdown statistics
    MAX_DRAWDOWN: str = 'max_drawdown'

    # Trade Statistics
    TRADES: str = 'trades'