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
        