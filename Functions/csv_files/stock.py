from ..config import API_KEY
from eod import EodHistoricalData
import random
from datetime import datetime as dt, timedelta
import os
import numpy as np
import pandas as pd
import typing
import pandas_ta as ta


class Stock:
    def __init__(self, symbol, start_date="1985-01-01", end_date="2022-12-31", filepath="csv_files/"):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.filepath = filepath
        self.data = None

        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)

    def retrieve_data(self):
        filepath = self.filepath + "stock/" + self.symbol + ".csv"

        dataframe = self.retrieve_prices_and_volume()
        dataframe = self.combine_3M_bills(dataframe)
        dataframe = self.combine_oil_prices(dataframe)
        for p in [7, 14]:
            dataframe = self.calc_rolling_volatility(dataframe, p)
            dataframe = self.calc_rolling_ewm(dataframe, p)
            dataframe = self.calc_rolling_rsi(dataframe, p)
            dataframe = self.calc_rolling_slope(dataframe, p)

        self.data = dataframe

        return self.data

    def retrieve_prices_and_volume(self):
        filepath = self.filepath + "stock/" + self.symbol + "_prices.csv"
        if os.path.exists(filepath):
            return pd.read_csv(filepath)

        client = EodHistoricalData(API_KEY)
        data = client.get_prices_eod(self.symbol.upper(),
                                     from_=self.start_date,
                                     to=self.end_date)

        dataframe = pd.DataFrame(data)[['date', 'close', 'volume']]

        dataframe.to_csv(filepath, index=False)
        print("Saved!")

        return dataframe

    def calc_rolling_volatility(self, dataframe, period):
        vol = dataframe['close'].rolling(period).std()*(252**0.5)
        df = dataframe.copy()
        df[f"{period}-day volatility"] = vol
        return df

    def calc_rolling_slope(self, dataframe, period):
        def slope(seri):
            return np.polyfit(x=seri.index.values, y=seri.values, deg=1)[0]

        df = dataframe.copy()
        df[f"{period}-day slope"] = df['close'].rolling(
            period).apply(slope, raw=False)
        return df

    def calc_rolling_ewm(self, dataframe, period):
        # https://corporatefinanceinstitute.com/resources/capital-markets/exponential-moving-average-ema/
        df = dataframe.copy()
        df[f"{period}-day EWM"] = df['close'].ewm(
            span=period, min_periods=0, adjust=False, ignore_na=False).mean()
        return df

    def calc_rolling_rsi(self, dataframe, period):
        df = dataframe.copy()
        df[f"{period}-rsi"] = ta.sma(df['close'], length=period)
        return df

    def combine_3M_bills(self, dataframe):
        bills = pd.read_csv(self.filepath + "3MTY.csv")
        df = dataframe.copy()
        df = df.merge(bills, on='date', how='left')
        return df

    def combine_oil_prices(self, dataframe):
        wti = pd.read_csv(self.filepath + "WTI.csv")
        df = dataframe.copy()
        df = df.merge(wti, on='date', how='left')
        return df


if __name__ == "__main__":
    stuff = Stock("AAPL.US").retrieve_data()
    print(stuff.head(30).to_string())
