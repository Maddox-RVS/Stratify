from datetime import datetime
from ... import stratify
import pickle

def test_downloadData():
    # Load static data from pickle file (this data should never change, as it is historical data)
    with open('tests/stratify/test_engine_downloadData_AAPL_20_1_1_24_1_1_data.pkl', 'rb') as pickleFile:
        historicalTickerFeedAAPL: stratify.TickerFeed = pickle.load(pickleFile)

    startDate: datetime = datetime(2020, 1, 1)
    endDate: datetime = datetime(2024, 1, 1)

    # Download actual historical data using yfinance, this should make sure the same data is always downloaded 
    tickerFeedAPPL: stratify.TickerFeed = stratify.downloadData('AAPL', startDate, endDate)

    # Compare the downloaded data with the static data
    assert isinstance(tickerFeedAPPL, stratify.TickerFeed), 'Downloaded data is not a TickerFeed'
    assert len(tickerFeedAPPL) == len(historicalTickerFeedAAPL), 'TickerFeed length mismatch'
    assert tickerFeedAPPL.getByFirstDate() == historicalTickerFeedAAPL.getByFirstDate(), 'First date mismatch'
    assert tickerFeedAPPL.getByLastDate() == historicalTickerFeedAAPL.getByLastDate(), 'Last date mismatch'