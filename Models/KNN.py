from Functions import api_technical, sp500
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

train, dev, test = sp500.get_sp500_tickers(split=True)

dataframes = []
for index, tickers in enumerate(train[:10]):
    print(f"Getting {index}/450")
    dataframes.append(api_technical.get_technical_data(tickers,
                                                       ['sma', 'ema', 'wma', 'volatility'],
                                                       '1980-01-01',
                                                       '2022-10-31',
                                                       period = 30,
                                                       with_prices=True))
df = pd.concat(dataframes).reset_index()
print(df)


"""
Idea: We use technical data from the past 30 days to feed into the data
"""

def pipeline():

