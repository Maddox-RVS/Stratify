from datetime import datetime
from ... import stratify
import copy

def test_TickerData():
    # Create a TickerData object with sample data
    tickerData: stratify.TickerData = stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000)

    # Check that the attributes are set correctly
    assert tickerData.ticker == 'AAPL'
    assert tickerData.dateTime == datetime(2001, 1, 1)
    assert tickerData.open == 100
    assert tickerData.close == 200
    assert tickerData.low == 50
    assert tickerData.high == 300
    assert tickerData.volume == 1000

    # Check the string representation
    assert str(tickerData) == 'TickerData(ticker=AAPL, dateTime=2001-01-01 00:00:00, open=100.00, close=200.00, low=50.00, high=300.00, volume=1000)', 'String representation does not match expected format'
    assert repr(tickerData) == 'TickerData(ticker=AAPL, dateTime=2001-01-01 00:00:00, open=100.00, close=200.00, low=50.00, high=300.00, volume=1000)', 'String representation does not match expected format'

    # Test equality
    equalTickerData: stratify.TickerData = copy.deepcopy(tickerData)
    assert tickerData == equalTickerData, 'Equal TickerData objects should be equal'

    # Test inequality with different ticker
    unequalTickerData: stratify.TickerData = stratify.TickerData(ticker='GOOGL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000)
    assert tickerData != unequalTickerData, 'Unequal TickerData objects should not be equal'

    unequalTickerData = stratify.TickerData(ticker='AAPL', dateTime=datetime(2005, 1, 1), open=100, close=200, low=50, high=300, volume=1000)
    assert tickerData != unequalTickerData, 'Unequal TickerData objects should not be equal'

    unequalTickerData = stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=105, close=200, low=50, high=300, volume=1000)
    assert tickerData != unequalTickerData, 'Unequal TickerData objects should not be equal'

    unequalTickerData = stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=205, low=50, high=300, volume=1000)
    assert tickerData != unequalTickerData, 'Unequal TickerData objects should not be equal'

    unequalTickerData = stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=55, high=300, volume=1000)
    assert tickerData != unequalTickerData, 'Unequal TickerData objects should not be equal'

    unequalTickerData = stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=305, volume=1000)
    assert tickerData != unequalTickerData, 'Unequal TickerData objects should not be equal'

    unequalTickerData = stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1005)
    assert tickerData != unequalTickerData, 'Unequal TickerData objects should not be equal'

def test_TickerFeed():
    # Create an empty TickerFeed
    tickerFeed: stratify.TickerFeed = stratify.TickerFeed()

    # Check that the feed is empty
    assert len(tickerFeed) == 0, 'New TickerFeed should be empty'
    assert tickerFeed.feed == [], 'New TickerFeed should have an empty feed'

    # Check the string representation of an empty TickerFeed
    assert str(tickerFeed) == 'TickerFeed:{Empty}', 'String representation of empty TickerFeed should be "TickerFeed:{Empty}"'

    # Add some sample data to tickerFeed
    tickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000)) # 1
    tickerFeed.append(stratify.TickerData(ticker='GOOG', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000)) # 2
    tickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2005, 1, 1), open=100, close=200, low=50, high=300, volume=1000)) # 3
    tickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=105, close=200, low=50, high=300, volume=1000)) # 4
    tickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=205, low=50, high=300, volume=1000)) # 5
    tickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=55, high=300, volume=1000)) # 6
    tickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=305, volume=1005)) # 7
    tickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000)) # 8

    # Check that the feed has the correct number of items
    assert len(tickerFeed) == 8, 'TickerFeed should contain 8 items after appending 8 TickerData objects'

    # Check the string representation of the TickerFeed
    assert tickerFeed.feed[0] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000), 'First item in TickerFeed should match the first appended TickerData'
    assert tickerFeed.feed[1] == stratify.TickerData(ticker='GOOG', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000), 'Second item in TickerFeed should match the second appended TickerData'
    assert tickerFeed.feed[2] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2005, 1, 1), open=100, close=200, low=50, high=300, volume=1000), 'Third item in TickerFeed should match the third appended TickerData'
    assert tickerFeed.feed[3] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=105, close=200, low=50, high=300, volume=1000), 'Fourth item in TickerFeed should match the fourth appended TickerData'
    assert tickerFeed.feed[4] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=205, low=50, high=300, volume=1000), 'Fifth item in TickerFeed should match the fifth appended TickerData'
    assert tickerFeed.feed[5] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=55, high=300, volume=1000), 'Sixth item in TickerFeed should match the sixth appended TickerData'
    assert tickerFeed.feed[6] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=305, volume=1005), 'Seventh item in TickerFeed should match the seventh appended TickerData'
    assert tickerFeed.feed[7] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000), 'Eighth item in TickerFeed should match the eighth appended TickerData'

    # Check the earliest and latest dates in the TickerFeed
    assert tickerFeed.getByFirstDate() == datetime(2001, 1, 1), 'Earliest date in TickerFeed should be 2001-01-01'
    assert tickerFeed.getByLastDate() == datetime(2005, 1, 1), 'Latest date in TickerFeed should be 2005-01-01'

    # Check for equality with another TickerFeed
    equalTickerFeed: stratify.TickerFeed = copy.deepcopy(tickerFeed)
    assert tickerFeed == equalTickerFeed, 'TickerFeed should be equal to its copy'

    # Check for inequality with a different TickerFeed
    unequalTickerFeed: stratify.TickerFeed = stratify.TickerFeed()
    unequalTickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000)) # 1
    unequalTickerFeed.append(stratify.TickerData(ticker='GOOG', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000)) # 2
    unequalTickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2005, 1, 1), open=100, close=200, low=50, high=300, volume=1000)) # 3
    unequalTickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=105, close=4000, low=50, high=300, volume=1000)) # 4
    unequalTickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=205, low=50, high=300, volume=1000)) # 5
    unequalTickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=55, high=300, volume=1000)) # 6
    unequalTickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=305, volume=1005)) # 7
    unequalTickerFeed.append(stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000)) # 8
    assert tickerFeed != unequalTickerFeed, 'TickerFeed should not be equal to a different TickerFeed with different data'

    # Check iteration over TickerFeed
    tickerDataList: list[stratify.TickerData] = [tickerData for tickerData in tickerFeed]
    assert len(tickerDataList) == 8, 'Iterating over TickerFeed should yield 8 TickerData items'

    assert tickerDataList[0] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000), 'First item in iteration should match the first appended TickerData'
    assert tickerDataList[1] == stratify.TickerData(ticker='GOOG', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000), 'Second item in iteration should match the second appended TickerData'
    assert tickerDataList[2] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2005, 1, 1), open=100, close=200, low=50, high=300, volume=1000), 'Third item in iteration should match the third appended TickerData'
    assert tickerDataList[3] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=105, close=200, low=50, high=300, volume=1000), 'Fourth item in iteration should match the fourth appended TickerData'
    assert tickerDataList[4] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=205, low=50, high=300, volume=1000), 'Fifth item in iteration should match the fifth appended TickerData'
    assert tickerDataList[5] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=55, high=300, volume=1000), 'Sixth item in iteration should match the sixth appended TickerData'
    assert tickerDataList[6] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=305, volume=1005), 'Seventh item in iteration should match the seventh appended TickerData'
    assert tickerDataList[7] == stratify.TickerData(ticker='AAPL', dateTime=datetime(2001, 1, 1), open=100, close=200, low=50, high=300, volume=1000), 'Eighth item in iteration should match the eighth appended TickerData'
    
    # Check the string representation of the TickerFeed
    assert str(tickerFeed) == 'TickerFeed:{TickerData(ticker=AAPL, dateTime=2001-01-01 00:00:00, open=100.00, close=200.00, low=50.00, high=300.00, volume=1000) ... 6 others ... TickerData(ticker=AAPL, dateTime=2001-01-01 00:00:00, open=100.00, close=200.00, low=50.00, high=300.00, volume=1000)}', 'String representation of TickerFeed does not match expected format'
    assert repr(tickerFeed) == 'TickerFeed:{TickerData(ticker=AAPL, dateTime=2001-01-01 00:00:00, open=100.00, close=200.00, low=50.00, high=300.00, volume=1000) ... 6 others ... TickerData(ticker=AAPL, dateTime=2001-01-01 00:00:00, open=100.00, close=200.00, low=50.00, high=300.00, volume=1000)}', 'String representation of TickerFeed does not match expected format'

    tickerFeed.feed = tickerFeed.feed[:2]
    assert len(tickerFeed) == 2, 'TickerFeed should contain 2 items after slicing to first 2 items'

    assert str(tickerFeed) == 'TickerFeed:{TickerData(ticker=AAPL, dateTime=2001-01-01 00:00:00, open=100.00, close=200.00, low=50.00, high=300.00, volume=1000), TickerData(ticker=GOOG, dateTime=2001-01-01 00:00:00, open=100.00, close=200.00, low=50.00, high=300.00, volume=1000)}', 'String representation of TickerFeed with 2 items does not match expected format'
    assert repr(tickerFeed) == 'TickerFeed:{TickerData(ticker=AAPL, dateTime=2001-01-01 00:00:00, open=100.00, close=200.00, low=50.00, high=300.00, volume=1000), TickerData(ticker=GOOG, dateTime=2001-01-01 00:00:00, open=100.00, close=200.00, low=50.00, high=300.00, volume=1000)}', 'String representation of TickerFeed with 2 items does not match expected format'

    tickerFeed.feed = tickerFeed.feed[:1]
    assert len(tickerFeed) == 1, 'TickerFeed should contain 1 item after slicing to first item'

    assert str(tickerFeed) == 'TickerFeed:{TickerData(ticker=AAPL, dateTime=2001-01-01 00:00:00, open=100.00, close=200.00, low=50.00, high=300.00, volume=1000)}', 'String representation of TickerFeed with 1 item does not match expected format'
    assert repr(tickerFeed) == 'TickerFeed:{TickerData(ticker=AAPL, dateTime=2001-01-01 00:00:00, open=100.00, close=200.00, low=50.00, high=300.00, volume=1000)}', 'String representation of TickerFeed with 1 item does not match expected format'
    
def test_Position():
    # Create a Position object with sample data
    position: stratify.data.Position = stratify.data.Position(ticker='AAPL', units=10)

    # Check that the attributes are set correctly
    assert position.ticker == 'AAPL', 'Ticker should be set correctly'
    assert position.units == 10, 'Units should be set correctly'

    # Check proper initialization with default units
    position = stratify.data.Position(ticker='GOOG')
    assert position.ticker == 'GOOG', 'Ticker should be set correctly'
    assert position.units == 0, 'Default units should be 0'

    # Check string representation
    assert str(position) == 'Position(ticker=\'GOOG\', units=0)', 'String representation does not match expected format'
    assert repr(position) == 'Position(ticker=\'GOOG\', units=0)', 'String representation does not match expected format'

    # Check equality
    equalPosition: stratify.data.Position = copy.deepcopy(position)
    assert position == equalPosition, 'Equal Position objects should be equal'

    # Check inequality with different ticker
    unequalPosition: stratify.data.Position = stratify.data.Position(ticker='AAPL', units=10)
    assert position != unequalPosition, 'Unequal Position objects should not be equal'