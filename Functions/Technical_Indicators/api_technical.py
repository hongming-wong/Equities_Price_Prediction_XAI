import pandas as pd
from Functions.config import API_KEY
from eod import EodHistoricalData

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


def get_technical_data(symbol, indicator, start, end, period=50):
    """
    Calls the api and returns a dataframe
    """
    try:
        data = client.get_instrument_ta(symbol,
                                        function=indicator,
                                        from_=start,
                                        to=end,
                                        period=period)
        df = pd.DataFrame(data)
        return df

    except Exception as ex:
        print("Something wrong with the parameters given")
        print(ex)


print(get_technical_data('MSFT.US', 'bbands', '2022-01-01', '2022-08-31'))




