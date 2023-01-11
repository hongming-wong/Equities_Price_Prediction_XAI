import pandas as pd
from Functions.config import API_KEY
from eod import EodHistoricalData
from Functions.Historical_Prices import historical_prices

client = EodHistoricalData(API_KEY)

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


def get_technical_data(symbol, indicator, start, end, with_prices=False, **kwargs):
    """
    Calls the api and returns a dataframe
    """
    try:
        if isinstance(indicator, str):
            data = client.get_instrument_ta(symbol.upper(),
                                            function=indicator.lower(),
                                            from_=start,
                                            to=end,
                                            **kwargs)
            df = pd.DataFrame(data)
        else:
            df = None
            for i in indicator:
                data = client.get_instrument_ta(symbol.upper(),
                                                function=i.lower(),
                                                from_=start,
                                                to=end,
                                                **kwargs)
                if df is None:
                    df = pd.DataFrame(data)
                else:
                    df = df.merge(pd.DataFrame(data), on='date', how='left')

        if with_prices:
            prices = historical_prices.get_eod_prices(symbol.upper(),
                                                      start,
                                                      end,
                                                      **kwargs)

            df = df.merge(prices, on='date', how='left')

        return df

    except Exception as ex:
        print("Something wrong with the parameters given")
        print(ex)


# f1 = get_technical_data('AAPL.US', ['sma', 'ema', 'slope'], '2022-01-01', '2022-08-31', with_prices=True)
# print(f1)
