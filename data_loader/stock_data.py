# Author: Xavier O'Rourke Goby

import pandas_datareader as web
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class StockData:
    from datetime import datetime

    source = "yahoo"

    def __init__(self, ticker_index, end_date=datetime.today().strftime("%m-%d-%Y"), start_date="01/06/2014"):
        self.ticker_index = ticker_index
        self.start_date = start_date
        self.end_date = end_date
        self.stock_data_df = self.get_stocks_data()
        self.index = self.stock_data_df.index
        self.dates = self.stock_data_df["Dates"]
        self.high = self.stock_data_df["High"]
        self.low = self.stock_data_df["Low"]
        self.open = self.stock_data_df["Open"]
        self.close = self.stock_data_df["Close"]
        self.volume = self.stock_data_df["Volume"]
        self.adj_close = self.stock_data_df["Adj Close"]


    def __str__(self):
        return ": ".join(["The indicator/ticker of the company this data belongs to is", self.ticker_index])


    # def get_stocks_data(sstock_idx = "AAPL", start_date = "01/06/2014", end_date = "12/10/2018"):
    def get_stocks_data(self):

        """
        Requires the pandas-datareader library
        :param stock_idx: str of yahoo index be default is "AAPL"
        :param start_date: str with format mm/dd/YYYY  (so "%m-%d-%Y") by default is "01/06/2014"
        "left end date", "oldest date"
        :param end_date: str with format mm/dd/YYY (so "%m-%d-%Y") by default is "01/06/2014" "12/03/2018"
        "right end date", "most recent date"
        :return: A pandas.core.frame.DataFrame with cols ['Dates', 'High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close']
        The index of the DataFrame is a pandas.core.indexes.datetimes.DatetimeIndex obj w/ the date stamp corresponding to
        row AKA "bar" of the table.
        The 'Dates' col is a pandas.core.series.Series type obj with it's elements being pandas._libs.tslibs.timestamps.Timestamp type objects
        """

        source = 'yahoo'
        data = web.DataReader(self.ticker_index,data_source=source, start=self.start_date, end=self.end_date)
        # wk_days = [d.strftime("%A") for d in data.index.date]
        datetime_dates_list = data.index.date.tolist()
        # data.insert(0, "WeekDays", wk_days)
        data.insert(0, "Dates", datetime_dates_list)
        # data.insert(0, "Dates", wk_days)
        return data


    def get_ema_smooth_stocks_data(self, trend_period=21):
        data = self.get_stocks_data()
        # datetime_dates_list = data.index.date.tolist()
        un_smooth_close = data["Close"]
        smooth_close = un_smooth_close.ewm(span=trend_period).mean()
        data["Close"] = smooth_close
        # data.insert(0, "Dates", datetime_dates_list)
        return data

