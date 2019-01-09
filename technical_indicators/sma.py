import pandas as pd
import numpy as np


class SMA:

    def __init__(self, close, ticker_index, trend_period_days=21):
        self.ticker_index = ticker_index
        # self.stock_data = StockData(ticker_index)
        self.close = close
        # self.close = self.stock_data.close
        self.trend_period = trend_period_days
        # self.trend_period_name = "SMA" + str(self.trend_period) + "d"
        self.trend_period_name = "SMA"
        self.sma_trend = self.compute_and_get_sma_signal_values()

    def __str__(self):
        meta_info = "\nSimple Moving Average (SMA) Parameters Information:\
        \nThe company stock data ticker/index is: {0}\
        \nThe trend period is: {1}".format(self.ticker_index, self.trend_period)
        return meta_info

    def compute_sma(self):
        dt_dates_list = self.close.index.date.tolist()
        trend = self.close.rolling(window=self.trend_period).mean()
        sma_trend = pd.DataFrame({"Dates":dt_dates_list, "Close":self.close.values,
                                  self.trend_period_name:trend.values}, index=range(len(dt_dates_list)))
        return sma_trend

    def compute_and_get_sma_signal_values(self):
        dt_dates_list = self.close.index.date.tolist()
        # trend = self.close.rolling(window=self.trend_period).mean()
        trend = np.round(self.close.rolling(window=self.trend_period).mean(), 4)
        trend = trend.dropna()
        trend.rename(self.trend_period_name)
        return trend

    def get_sma_values(self):
        return self.sma_trend[self.trend_period_name]

