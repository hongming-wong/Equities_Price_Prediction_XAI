from Functions.sp500.sp500 import get_sp500_tickers
from Functions.config import API_KEY
from eod import EodHistoricalData
import random
from datetime import datetime as dt, timedelta
from Functions.Technical_Indicators.api_technical import get_technical_data
import os
import numpy as np
import pandas as pd

RANGE_START = dt(1990, 1, 1).timestamp()
RANGE_END = dt(2022, 10, 31).timestamp()


def random_date(range_start=RANGE_START, range_end=RANGE_END):
    return random.randint(int(range_start), int(range_end))


def timestamp_to_string(timestamp):
    return dt.fromtimestamp(timestamp).strftime('%Y-%m-%d')


def sample(symbol, no_samples=25):
    TI = ['wma', 'slope', 'rsi', 'volatility']
    COLUMNS = ['date', 'adjusted_close', 'volume'] + TI
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

            X = data.head(14)[COLUMNS]
            y = data.iloc[[15]]['adjusted_close'].item()
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


def save_data(ticker, X, y=None, folder_name=''):
    if not os.path.exists(f"{folder_name}/{ticker}"):
        os.makedirs(f"{folder_name}/{ticker}")
    np.save(f"{folder_name}/{ticker}/X", X)
    np.save(f"{folder_name}/{ticker}/y", y)


def load_data(tickers, folder_name):
    final_X, final_y = None, None
    for ticker in tickers:
        print(f"Loading {ticker}")

        if not os.path.exists(f"{folder_name}/{ticker}/X.npy") or \
                not os.path.exists(f"{folder_name}/{ticker}/y.npy"):
            print(f"No {ticker} data")
            continue

        data_X = np.load(f"{folder_name}/{ticker}/X.npy", allow_pickle=True)
        data_y = np.load(f"{folder_name}/{ticker}/y.npy", allow_pickle=True)
        if final_X is None and final_y is None:
            final_X = data_X
            final_y = data_y
        else:
            final_X = np.append(final_X, data_X, axis=0)
            final_y = np.append(final_y, data_y, axis=0)
    return final_X, final_y


def load_without_y(tickers, folder_name):
    final_X = None
    for ticker in tickers:
        print(f"Loading {ticker}")

        if not os.path.exists(f"{folder_name}/{ticker}/X.npy"):
            print(f"No {ticker} data")
            continue
        data_X = np.load(f"{folder_name}/{ticker}/X.npy", allow_pickle=True)
        if final_X is None:
            final_X = data_X
        else:
            final_X = np.append(final_X, data_X, axis=0)
    return final_X


def sampling_from_scratch(tickers):
    total = len(tickers)
    """
    As of 30th December 2022, tickers above WTW.US are not downloaded yet because we hit the API limit.
    But we have 6675 training data so it should be sufficient. 
    """
    for index, ticker in enumerate(tickers):
        if os.path.exists(f"sampling_data/{ticker}/X.npy"):
            print(f"skipping {ticker}")
            continue
        print(f"{index}/{total} - Collecting Data for {ticker}")
        X, y = sample(ticker)
        print(f"Saving Data for {ticker}")
        save_data(ticker, X, y, folder_name='sampling_data')


def feature_addition(TI, period, source_folder_name, new_folder_name):
    tickers = get_sp500_tickers(False)
    end = tickers.index("WTW.US")
    tickers = tickers[:end]

    client = EodHistoricalData(API_KEY)

    for ticker in tickers:
        if os.path.exists(f"{new_folder_name}/{ticker}/X.npy"):
            print(f"skipping {ticker}")
            continue

        print(f"Dealing with {ticker}")
        x = load_without_y([ticker], source_folder_name)
        if x is None or len(x.shape) != 3 or x.shape[1] != 14:
            print(f"{ticker} is corrupted: Training Data is incorrect")
            continue
        x_new = []
        for index, item in enumerate(x):
            start_date = item[0, 0]
            end_date = item[-1, 0]
            data = get_technical_data(client,
                                      ticker,
                                      TI,
                                      start_date,
                                      end_date,
                                      period=period,
                                      price=False)
            x_new.append(pd.DataFrame(item).merge(data[['date'] + TI], left_on=0, right_on='date', how='left'))
        save_data(ticker, np.array(x_new), folder_name=new_folder_name)
        print(f"Complete {ticker}")


if __name__ == "__main__":
    sampling_from_scratch(get_sp500_tickers())
    features_26 = ['wma', 'slope', 'rsi', 'dmi', 'sar']
    feature_addition(features_26, 26, 'sampling_data', 'sampling_data_2')
    # features_7 = ['wma', 'slope', 'rsi']
    # feature_addition(features_7, 7, 'sampling_data_2', 'sampling_data_3')
    # data = load_without_y(get_sp500_tickers(), 'sampling_data_2')
    # print(data.shape)
