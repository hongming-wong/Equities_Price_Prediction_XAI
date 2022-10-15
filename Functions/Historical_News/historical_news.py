import pandas as pd
from Functions.sp500 import sp500
from Functions.config import API_KEY
from Functions.Historical_Prices import historical_prices
from eod import EodHistoricalData
import requests

client = EodHistoricalData(API_KEY)

tickers = sp500.get_sp500_tickers()


def get_news_by_ticker(ticker, start, end, offset=0, limit=10):
    """
    Get news data for a specific stock in the format of dataframe (columns = date, content)
    """
    try:
        response = requests.get(
            f'https://eodhistoricaldata.com/api/news?api_token={API_KEY}&s={ticker}&from={start}&to={end}&offset={offset}&limit={limit}')
        data = pd.read_json(response.text).loc[:, ['date', 'content']]
        data['date'] = pd.to_datetime(data['date'].dt.strftime('%Y-%m'))
        # output = []
        # for para in data.to_list():
        #     result = ''
        #     sentences = para.split('\n')
        #     for sentence in sentences:
        #         result += ' ' + sentence
        #     output.append(result)
        # df = pd.DataFrame(data.set_index('date').T.to_dict('list'))
        return data

    except Exception as ex:
        print("Error getting the news")
        print(ex)


def get_news_to_price_changes(ticker, start, end, offset=0, limit=100, period=50):
    """
    Get news to price change for a specific stock in the format of dataframe (columns = date, content, price_change)
    """
    news = get_news_by_ticker(ticker, start, end, offset, limit)
    price = historical_prices.get_daily_price_changes(ticker, start, end, period)

    for t, p in price.items():
        news.loc[news['date'] == pd.to_datetime(t), 'price_change'] = p

    return news

# print(get_news_to_price_changes('MSFT.US', '2021-01-03', '2022-01-05'))
