import pandas as pd
from Functions.SP500 import sp500
from Functions.config import API_KEY
from eod import EodHistoricalData

client = EodHistoricalData(API_KEY)

tickers = sp500.get_sp500_tickers()

def get_sentiment(ticker, start, end):
    """
    Get sentiment score of news computed by eod for a specific stock
    """
    try:
        data = client.get_sentiment(s=ticker, from_=start, to=end)
        return data

    except Exception as ex:
        print("Error getting the sentiment of the news")
        print(ex)

def get_news_by_ticker(ticker, start, end, limit=50):
    """
    Get news data for a specific stock
    """
    try:
        data = client.get_financial_tweets(s=ticker, from_=start, to=end, limit=limit)
        return data

    except Exception as ex:
        print("Error getting the news")
        print(ex)


print(get_news_by_ticker('AAPL.US', '2020-01-05', '2020-10-10'))
