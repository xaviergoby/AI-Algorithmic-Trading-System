import pandas as pd
from stock_data import StockData


class EMA:

    def __init__(self, ticker_index, trend_period_days=21):
        self.ticker_index = ticker_index
        self.stock_data = StockData(ticker_index)
        self.close = self.stock_data.close
        self.trend_period = trend_period_days
        self.ema_trend = self.compute_ema()

    def __str__(self):
        meta_info = "\nExponential Moving Average (EMA) Parameters Information:\
        \nThe company stock data ticker/index is: {0}\
        \nThe trend period is: {1}".format(self.ticker_index, self.trend_period)
        return meta_info

    def compute_ema(self):
        """
        Exponential Moving Average
        """
        trend_period_name = str(self.trend_period) + "d"
        dt_dates_list = self.close.index.date.tolist()
        trend = self.close.ewm(span=self.trend_period).mean()
        ema_trend = pd.DataFrame({"Dates": dt_dates_list, "Close": self.close.values, "EMA": trend.values},
                                 index=range(len(dt_dates_list)))
        return ema_trend

