import pandas as pd
from Functions.Historical_Prices import historical_prices
import traceback
import datetime as dt
import numpy as np

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


def get_technical_data(client, symbol, indicator, start, end, period=14, price=True, verbose=False, **kwargs):
    """
    Calls the api and returns a dataframe
    """

    t_start = dt.datetime.strptime(start, "%Y-%m-%d") - dt.timedelta(days=2 * period)
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

            if data is None or len(data) == 0:
                if df is None:
                    df = pd.DataFrame(np.nan, index=range(14), columns=[i.lower()])
                else:
                    df[i.lower()] = np.nan
            else:
                if df is None:
                    df = pd.DataFrame(data)
                else:
                    data = pd.DataFrame(data)
                    if 'date' not in df.columns:
                        for column in df.columns:
                            data[column] = np.nan
                        cols = ['date'] + list(df.columns) + [i.lower()]
                        df = data[cols]
                    else:
                        df = df.merge(data, on='date', how='left')
    if price:
        prices = historical_prices.get_eod_prices(symbol.upper(), start, end)
        if 'date' not in df.columns:
            for column in df.columns:
                prices[column] = np.nan
            df = prices
        else:
            df = df.merge(prices, on='date', how='inner')

    return df


if __name__ == '__main__':

    from eod import EodHistoricalData
    from Functions.config import API_KEY

    client = EodHistoricalData(API_KEY)
    f1 = get_technical_data(client,
                            'META.US',
                            ['macd', 'sma'],
                            '2012-05-21',
                            '2012-06-04',
                            period=2)
    print(f1)
