import pandas as pd
from Functions.Historical_Prices import historical_prices
import traceback
import datetime as dt

ta_indicators = {
    'splitadjusted': 'Split Adjusted Data',
    'avgvol': 'Average Volume',
    'avgvolccy': 'Average Volume by Price',
    'sma': 'Simple Moving Average',
    'ema': 'Exponential Moving Average',
    'wma': 'Weighted Moving Average',
    'volatility': 'Variance between returns',
    'stochastic': 'Stochastic Technical Indicator',
    'rsi': 'Relative Strength Index',
    'stddev': 'Standard Deviation',
    'stochrsi': 'Stochastic Relative Strength Index',
    'slope': 'Linear Regression',
    'dmi': 'Directional Movement Index',
    'adx': 'Average Directional Movement Index',
    'macd': 'Moving Average Convergence/Divergence',
    'atr': 'Average True Range',
    'cci': 'Commodity Channel Index',
    'sar': 'Parabolic SAR',
    'bbands': 'Bollinger Bands'
}


def get_technical_data(client, symbol, indicator, start, end, period=14, verbose=False, **kwargs):
    """
    Calls the api and returns a dataframe
    """

    t_start = dt.datetime.strptime(start, "%Y-%m-%d") - dt.timedelta(days=2 * period)
    try:
        if isinstance(indicator, str):
            data = client.get_instrument_ta(symbol.upper(),
                                            function=indicator.lower(),
                                            from_=t_start,
                                            to=end,
                                            period=period,
                                            **kwargs)
            df = pd.DataFrame(data)
        else:
            df = None
            for i in indicator:
                data = client.get_instrument_ta(symbol.upper(),
                                                function=i.lower(),
                                                from_=t_start,
                                                to=end,
                                                period=period,
                                                **kwargs)
                if df is None:
                    df = pd.DataFrame(data)
                else:
                    df = df.merge(pd.DataFrame(data), on='date', how='left')

        prices = historical_prices.get_eod_prices(symbol.upper(), start, end)

        df = df.merge(prices, on='date', how='inner')

        return df

    except Exception as ex:
        if verbose:
            print("Something wrong with the parameters given")
            print(traceback.format_exc())


# from eod import EodHistoricalData
# from Functions.config import API_KEY
#
# client = EodHistoricalData(API_KEY)
# f1 = get_technical_data(client, 'AAPL.US', ['sma', 'ema', 'slope'], '2009-01-01', '2009-02-20')
# print(f1)