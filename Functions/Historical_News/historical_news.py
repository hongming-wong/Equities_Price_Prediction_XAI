import pandas as pd
from Functions.SP500 import sp500
from Functions.config import API_KEY
from eod import EodHistoricalData

client = EodHistoricalData(API_KEY)

tickers = sp500.get_sp500_tickers()

def get_news(ticker, start, end):

    try:
        data = client.get_sentiment(s=ticker, from_=start, to=end)
        df = pd.DataFrame(data)
        return df

    except Exception as ex:
        print("Error getting the news")
        print(ex)

print(get_news('AAPL.US', '2020-01-05', '2020-10-10'))
