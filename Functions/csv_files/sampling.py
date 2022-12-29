from Functions.sp500.sp500 import get_sp500_tickers
from Functions.config import API_KEY
from eod import EodHistoricalData
import random
from datetime import datetime as dt, timedelta
from Functions.Technical_Indicators.api_technical import get_technical_data
import os
import numpy as np

TI = ['sma', 'slope', 'rsi', 'volatility']
RANGE_START = dt(1985, 1, 1).timestamp()
RANGE_END = dt(2022, 10, 31).timestamp()


def random_date(range_start=RANGE_START, range_end=RANGE_END):
    return random.randint(int(range_start), int(range_end))


def timestamp_to_string(timestamp):
    return dt.fromtimestamp(timestamp).strftime('%Y-%m-%d')


def collect_data(symbol, no_samples=25):
    client = EodHistoricalData(API_KEY)
    X_samples = []
    y_samples = []
    counter = 0
    failed = 0
    range_start = RANGE_START
    while counter < no_samples:
        start_dt = random_date(range_start)
        end_dt = start_dt + timedelta(days=40).total_seconds()
        start_date, end_date = timestamp_to_string(start_dt), timestamp_to_string(end_dt)
        try:
            data = get_technical_data(client,
                                      symbol,
                                      TI,
                                      start_date,
                                      end_date)

            X = data.head(14)[['date', 'close'] + TI]
            y = data.iloc[[15]].close.item()
            X_samples.append(X.to_numpy())
            y_samples.append(y)
            counter += 1
            print(f"{counter} out of {no_samples}")

        except Exception:
            failed += 1
            print(f"The stock {symbol} might not be listed during this dates f{start_date} - f{end_date}")
            range_start = start_dt
            if failed > no_samples:
                print(f"Too many failures!")
                return None, None

    return np.array(X_samples), np.array(y_samples)


def save_data(ticker, X, y):
    if not os.path.exists(f"sampling_data/{ticker}"):
        os.makedirs(f"sampling_data/{ticker}")
    np.save(f"sampling_data/{ticker}/X", X)
    np.save(f"sampling_data/{ticker}/y", y)


def load_data(tickers):
    final_X, final_y = None, None
    for ticker in tickers:
        print(f"Loading {ticker}")

        if not os.path.exists(f"sampling_data/{ticker}/X.npy") or\
                not os.path.exists(f"sampling_data/{ticker}/y.npy"):
            print(f"No {ticker} data")
            continue

        data_X = np.load(f"sampling_data/{ticker}/X.npy", allow_pickle=True)
        data_y = np.load(f"sampling_data/{ticker}/y.npy", allow_pickle=True)
        if final_X is None and final_y is None:
            final_X = data_X
            final_y = data_y
        else:
            final_X = np.append(final_X, data_X, axis=0)
            final_y = np.append(final_y, data_y, axis=0)
    return final_X, final_y


def sampling(tickers):
    for ticker in tickers:
        print(f"Collecting Data for {ticker}")
        X, y = collect_data(ticker)
        print(f"Saving Data for {ticker}")
        save_data(ticker, X, y)


if __name__ == "__main__":
    tickers = get_sp500_tickers(split=False)
    sampling(tickers)

    # X, y = load_data(tickers)
    # print(X.shape)
    # print(y.shape)