import pandas as pd
from Functions.config import API_KEY
from eod import EodHistoricalData

client = EodHistoricalData(API_KEY)


def get_eod_prices(symbol, start, end, period=50):
    """
    Calls the api and returns a dataframe
    """
    try:
        data = client.get_prices_eod(symbol.upper(),
                                     from_=start,
                                     to=end,
                                     period=period)
        df = pd.DataFrame(data)
        return df

    except Exception as ex:
        print("Something wrong with the parameters given")
        print(ex)


def get_daily_price_changes(ticker, start, end, period=50):
    """
    Returns a dictionary of ticker to intraday price changes of a stock within a specific period in the format of { date : -1/0/1 } (0 = no data or price decreases, 1 = price increases)
    """
    try:
        price_diff = {}

        df = get_eod_prices(ticker, start, end, period)

        for index, row in df.iterrows():
            if index > 0:
                if row['adjusted_close'] - df.loc[index-1]['adjusted_close'] > 0:
                    price_diff[row['date']] = 1
                else:
                    price_diff[row['date']] = 0
            else:
                price_diff[row['date']] = 0

        return price_diff

    except Exception as ex:
        print("Error computing the daily price difference of the stock")
        print(ex)


# print(get_daily_price_changes('MSFT.US', '2021-01-05', '2021-02-10'))