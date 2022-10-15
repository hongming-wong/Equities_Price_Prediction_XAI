from Functions.Technical_Indicators import api_technical
from Functions.sp500 import sp500

start = '2000-01-01'
end = '2021-12-31'

train, dev, test = sp500.get_sp500_tickers(split=True)
dev = dev[:4]

periods = [30, 50, 100]
ta = ['sma', 'ema', 'wma', 'volatility', 'stochastic', 'slope']


def download(tickers, period, prefix=""):
    for ticker in tickers:
        api_technical.get_technical_data(ticker, ta, start, end, period=period).\
            to_csv(f"technical_data/{prefix}_period_{period}.csv")


for p in periods:
    download(dev, period=p, prefix="dev")
    print("Finish Downloading Dev")
    download(test, period=p, prefix="test")
    print("Finish Downloading Test")
    download(train, period=p, prefix="train")
    print("Finish Downloading Train")
