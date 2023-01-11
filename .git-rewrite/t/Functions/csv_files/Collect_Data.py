from Functions.Historical_Prices.historical_prices import get_eod_prices
from Functions.sp500 import sp500
import pandas as pd

start = '1975-01-01'
end = '2021-12-31'
train, dev, test = sp500.get_sp500_tickers(split=True)
train_df = []
dev_df = []
test_df = []

print("=== Downloading dev set ===")
for index, tickers in enumerate(dev):
    print(f"{index + 1} out of {len(dev)}")
    try:
        df = get_eod_prices(tickers, start, end)
        df['ticker'] = tickers
        dev_df.append(df)

    except:
        print('Something wrong with ticker', tickers)

dev_df = pd.concat(dev_df)
dev_df.to_csv('prices/dev.csv', index=False)

print("=== Downloading test set ===")
for index, tickers in enumerate(test):
    print(f"{index + 1} out of {len(test)}")
    try:
        df = get_eod_prices(tickers, start, end)
        df['ticker'] = tickers
        test_df.append(df)

    except:
        print('Something wrong with ticker', tickers)

test_df = pd.concat(test_df)
test_df.to_csv('prices/test.csv', index=False)

print("=== Downloading train set ===")
for index, tickers in enumerate(train):
    print(f"{index + 1} out of {len(train)}")
    try:
        df = get_eod_prices(tickers, start, end)
        df['ticker'] = tickers
        train_df.append(df)

    except:
        print('Something wrong with ticker', tickers)

train_df = pd.concat(train_df)
train_df.to_csv('prices/train.csv', index=False)

