from Functions.Technical_Indicators import api_technical
from Functions.sp500 import sp500
import os

start = '1995-01-01'
end = '2021-12-31'

train, dev, test = sp500.get_sp500_tickers(split=True)

train = train[:200]
periods = [100]
ta = ['sma', 'ema', 'wma', 'volatility', 'stochastic', 'slope']


def download(tickers, period, prefix=""):
    path = f"technical_data/{prefix}_period_{period}.csv"
    for ticker in tickers:
        print("Downloading", ticker)
        data = api_technical.get_technical_data(ticker, ta, start, end, period=period)
        data['ticker'] = ticker
        data.to_csv(path, mode='a', header=not os.path.exists(path), index=False)


for p in periods:
    print(f"Downloading for period {p}")
    download(dev, period=p, prefix="dev")
    print("Finish Downloading Dev")
    download(test, period=p, prefix="test")
    print("Finish Downloading Test")
    download(train, period=p, prefix="train")
    print("Finish Downloading Train")
