from datetime import datetime
from ... import stratify

def test_BuyOrder():
    # Create a BuyOrder instance
    order: stratify.order.Order = stratify.order.BuyOrder('AAPL', 10)

    # Check if order values are set correctly
    assert order.ticker == 'AAPL'
    assert order.units == 10
    assert order.fillStatus == stratify.order.FillStatus.PENDING
    assert order.__portfolioCashImpact__ == 0.0
    assert isinstance(order.__openedStartTime__, datetime)
    assert order.__closedEndTime__ is None

    # Check cancel order
    order.cancel()
    assert order.fillStatus == stratify.order.FillStatus.CANCELLED

    # Check default units
    order = stratify.order.BuyOrder('GOOGL')
    assert order.units == 1

def test_SellOrder():
    # Create a SellOrder instance
    order: stratify.order.Order = stratify.order.SellOrder('AAPL', 10)

    # Check if order values are set correctly
    assert order.ticker == 'AAPL'
    assert order.units == 10
    assert order.fillStatus == stratify.order.FillStatus.PENDING
    assert order.__portfolioCashImpact__ == 0.0
    assert isinstance(order.__openedStartTime__, datetime)
    assert order.__closedEndTime__ is None

    # Check cancel order
    order.cancel()
    assert order.fillStatus == stratify.order.FillStatus.CANCELLED

    # Check default units
    order = stratify.order.SellOrder('GOOGL')
    assert order.units == 1

def test_CloseOrder():
    # Create a CloseOrder instance
    order: stratify.order.Order = stratify.order.CloseOrder('AAPL', 10)

    # Check if order values are set correctly
    assert order.ticker == 'AAPL'
    assert order.units == 10
    assert order.fillStatus == stratify.order.FillStatus.PENDING
    assert order.__portfolioCashImpact__ == 0.0
    assert isinstance(order.__openedStartTime__, datetime)
    assert order.__closedEndTime__ is None

    # Check cancel order
    order.cancel()
    assert order.fillStatus == stratify.order.FillStatus.CANCELLED

    # Check default units
    order = stratify.order.CloseOrder('GOOGL')
    assert order.units == 1