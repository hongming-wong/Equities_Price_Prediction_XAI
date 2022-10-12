from Functions import api_technical
from sklearn import tree

data = api_technical.get_technical_data('AAPL.US',
                                        ['sma', 'ema', 'wma', 'volatility'],
                                        '2022-01-01',
                                        '2022-08-31',
                                        with_prices=True)
data = data.drop(columns=['open', 'high', 'low', 'close', 'volume'])

