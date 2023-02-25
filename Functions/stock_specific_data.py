from config import API_KEY
from eod import EodHistoricalData
import random
from datetime import datetime as dt, timedelta
import os
import numpy as np
import pandas as pd
import typing


RANGE_START = dt(1990, 1, 1).timestamp()
RANGE_END = dt(2022, 10, 31).timestamp()
TI = ['wma', 'slope', 'rsi', 'volatility']


class Stock:
    def __init__(self, symbol, start_date, end_date, indicators, periods):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.indicators = indicators
        self.periods = periods

    def pipeline(self):
        self.download()

    def download(self):
        client = EodHistoricalData(API_KEY)
        data = client.get_prices_eod(self.symbol.upper(),
                                     from_=self.start_date,
                                     to=self.end_date)
        dataframe = pd.DataFrame(data)

        for indicator in self.indicators:
            for period in self.periods:
                print("Downloading", indicator, period)
                data = client.get_instrument_ta(self.symbol.upper(),
                                                function=indicator.lower(),
                                                from_=self.start_date,
                                                to=self.end_date,
                                                period=period)
                df = pd.DataFrame(data)
                df.add_prefix(f"{period}-")

                dataframe = dataframe.merge(df, on='date', how='right')

        print("Done")

        filepath = "csv_files/stock/"

        if not os.path.exists(filepath):
            os.makedirs(filepath)

        dataframe.to_csv(filepath + self.symbol + ".csv")
        print("Saved!")

        return dataframe


if __name__ == "__main__":
    Stock("AAPL.US", "1970-01-01", "2022-12-31", TI, [7, 14]).download()
