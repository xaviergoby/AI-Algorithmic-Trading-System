import pandas as pd
import numpy as np

class TATools:

    @staticmethod
    def sma(stock_data_df, stock_symbol, period=21):
        """
        STATUS: VERIFIED (with Investing.com) on NVDA between 10-06-2019 & 14-06-2019
        The Simple Moving Average (Rolling Window) Indicator
        :param stock_data_df: The original OHCLV and VWAP pandas DataFrame output of i.e. the data_loader.data_sources.get_stocks_data()
        :param stock_symbol: str of the stock symbol
        :param period: Int of the number of days in the time period for computing the trend line values. Is 21 by def
        :return: A pandas Series w/ index=DatetimeIndex & name (so Series_data_returned.name):
        "stock_symbol"_sma_"period"
        """
        feature_name = "{0}_sma_{1}d".format(stock_symbol, period)
        pd_dt_idx = stock_data_df.index
        trend = stock_data_df.Close.rolling(window=period).mean()
        sma_data = pd.Series(trend.values, index=pd_dt_idx, name=feature_name)
        return sma_data

    @staticmethod
    def ema(stock_data_df, stock_symbol, period=14):
        """
        STATUS: VERIFIED (with Investing.com) on NVDA between 10-06-2019 & 14-06-2019
        :param stock_data_df: The original OHCLV and VWAP pandas DataFrame output of i.e. the data_loader.data_sources.get_stocks_data()
        :param stock_symbol: str of the stock symbol
        :param period: Int of the number of days in the time period for computing the trend line values. Is 14 by def
        :return: A pandas Series w/ index=DatetimeIndex & name (so Series_data_returned.name):
        "stock_symbol"_ema_"period"
        """
        feature_name = "{0}_ema_{1}d".format(stock_symbol, period)
        pd_dt_idx = stock_data_df.index
        trend = stock_data_df['Close'].ewm(span=period, min_periods=period).mean()
        ema_data = pd.Series(trend, index=pd_dt_idx, name=feature_name)
        return ema_data


    @staticmethod
    def rsi(stock_data_df, stock_symbol, period=14):
        """
        STATUS: VERIFIED (with Investing.com) on NVDA between 10-06-2019 & 14-06-2019
        :param stock_data_df: The original OHCLV and VWAP pandas DataFrame output of i.e. the data_loader.data_sources.get_stocks_data()
        :param stock_symbol: str of the stock symbol
        :param period: Int of the number of days in the time period for computing the trend line values. Is 14 by def
        :return: A pandas Series w/ index=DatetimeIndex & name (so Series_data_returned.name):
        "stock_symbol"_rsi_"period"
        """
        feature_name = "{0}_rsi_{1}d".format(stock_symbol, period)
        delta = stock_data_df["Close"].diff()
        up, down = delta.copy(), delta.copy()

        up[up < 0] = 0
        down[down > 0] = 0

        roll_up = up.ewm(com=period - 1, adjust=False).mean()
        roll_down = down.ewm(com=period - 1, adjust=False).mean().abs()

        rsi = 100 - 100 / (1 + roll_up / roll_down)

        rsi.name = feature_name
        return rsi

