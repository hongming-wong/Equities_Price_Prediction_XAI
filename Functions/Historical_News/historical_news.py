import pandas as pd
from Functions.sp500 import sp500
from Functions.config import API_KEY
from Functions.Historical_Prices import historical_prices
from eod import EodHistoricalData
import requests
from datetime import date, timedelta

client = EodHistoricalData(API_KEY)

def get_news_by_ticker(ticker, start, end, offset=0, limit=1000):
    """
    Get news data for a specific stock in the format of dataframe (columns = date, content)
    """
    try:
        response = requests.get(
            f'https://eodhistoricaldata.com/api/news?api_token={API_KEY}&s={ticker}&from={start}&to={end}&offset={offset}&limit={limit}')
        data = pd.read_json(response.text).loc[:, ['date', 'content']]
        data['date'] = pd.to_datetime(data['date'].dt.strftime('%Y-%m-%d'))
        return pd.DataFrame(data)

    except Exception as ex:
        print("Error getting the news")
        print(ex)

def get_news_to_price_changes(ticker, start, end, offset=0, limit=1000, period=50):
    """
    Get news to price change for a specific stock in the format of dataframe (columns = date, content, price_change)
    """
    try:
        news = get_all_news_by_ticker(ticker, start, end, offset, limit)
        price = historical_prices.get_daily_price_changes(ticker, start, end, period)

        for t, p in price.items():
            news.loc[news['date'] == pd.to_datetime(t), 'price_change'] = p

        return news.dropna()
    
    except Exception as ex:
        print("Error getting the news to price changes")
        print(ex)

def daterange(start_date, end_date):
    """
    Get all the dates from start_date to end_date
    """
    try:
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)
    
    except Exception as ex:
        print("Error getting the news to price changes")
        print(ex)

def get_all_news_by_ticker(ticker, start, end, offset=0, limit=1000):
    """
    Get all the news from start to end of a specific stock
    """
    try:
        df = pd.DataFrame(columns=['date', 'content'])
        for single_date in daterange(start, end):
            cur = single_date.strftime("%Y-%m-%d")
            new_df = get_news_by_ticker(ticker, cur, cur, offset, limit)
            dup_df = df.append(new_df, ignore_index=True)
            df = dup_df
        return df

    except Exception as ex:
        print("Error getting all news for a single stock")
        print(ex)

def get_all_news(start, end, offset=0, limit=1000):
    """
    Get all the news from start to end of all stocks separated into train and test sets
    """
    try:
        tickers = sp500.get_sp500_tickers()
        train, test = tickers[:450], tickers[450:]
        train_df, test_df = pd.DataFrame(columns=['date', 'content']), pd.DataFrame(columns=['date', 'content'])
        for t in train:
            print(f'extracting news for {t} ...')
            new_df = get_news_to_price_changes(t, start, end, offset, limit)
            dup_df = train_df.append(new_df, ignore_index=True)
            train_df = dup_df
        for t in test:
            print(f'extracting news for {t} ...')
            new_df = get_news_to_price_changes(t, start, end, offset, limit)
            dup_df = test_df.append(new_df, ignore_index=True)
            test_df = dup_df
        
        return train_df, test_df

    except Exception as ex:
        print("Error getting all the news")
        print(ex)

# print(get_all_news('MSFT.US', date(2021, 6, 1), date(2021, 9, 30)))
# print(get_news_by_ticker('MSFT.US', '2021-11-10', '2021-11-10'))
