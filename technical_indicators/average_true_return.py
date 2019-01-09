import pandas as pd
import numpy as np


class ATR:

    def __init__(self, hlc, period_length=14):
        self.dates = hlc.index
        self.high = hlc.High
        self.low = hlc.Low
        self.close = hlc.Close
        self.period_length = period_length
        self.tr_ts_dict = {"Dates":[], "TR":[]}


    def compute_tr_components_and_get_max(self, day):
        """
        classical_age = high - low
        high_min_prev_close_mag = high - close_prev
        low_min_prev_close_mag = low - close_prev
        :return:
        """
        classical_rage = self.high[day] - self.low[day]
        high_min_prev_close_mag = abs(self.high[day] - self.close[day-1])
        low_min_prev_close_mag = abs(self.low[day] - self.close[day-1])
        tr_components_trio = [classical_rage, high_min_prev_close_mag, low_min_prev_close_mag]
        tr_max_component = max(tr_components_trio)
        return tr_max_component

    def create_tr_series(self):
        for day in range(1, len(self.close)):
            date = self.dates[day]
            tr = round(self.compute_tr_components_and_get_max(day), 2)
            self.tr_ts_dict["Dates"].append(date)
            self.tr_ts_dict["TR"].append(tr)
            self.tr_ts_dict["Dates"] = self.tr_ts_dict["Dates"]
        # atr_dates_index = pd.DatetimeIndex(sides.index)
        tr_df = pd.Series(data = self.tr_ts_dict["TR"], index = self.tr_ts_dict["Dates"])
        return tr_df

    def create_atr_series(self):
        tr_df = self.create_tr_series()
        tr_df = tr_df.rolling(self.period_length).mean()
        return tr_df

