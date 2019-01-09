import pandas as pd

class MACD:

    def __init__(self, close, signal_average=9, ema_days_upper=26, ema_days_lower=12):
        self.close = close
        self._ema_days_upper = ema_days_upper  #long period/slow/upper
        self._ema_days_lower = ema_days_lower  #short period/fast/lower
        self.signal_average = signal_average
        self.dt_dates_list = self.close.index.date.tolist()

    def get_macd_values_df(self):
        """Calculate MACD, MACD Signal and MACD difference

        :param df: pandas.DataFrame
        :param self.ema_days_upper: #long period/slow/upper
        :param self.ema_days_lower: #short period/fast/lower
        :return: pandas.DataFrame
        """
        EMAfast = self.close.ewm(span=self._ema_days_upper, min_periods=self._ema_days_lower).mean()
        EMAslow = self.close.ewm(span=self._ema_days_lower, min_periods=self._ema_days_lower).mean()
        MACD = pd.Series(EMAfast - EMAslow, name='MACD_' + str(self._ema_days_upper) + '_' + str(self._ema_days_lower))
        MACDsign = pd.Series(MACD.ewm(span=self.signal_average, min_periods=self.signal_average).mean(), name='MACDsign_' + str(self._ema_days_upper) + '_' + str(self._ema_days_lower))
        MACDdiff = pd.Series(MACD - MACDsign, name='MACDdiff_' + str(self._ema_days_upper) + '_' + str(self._ema_days_lower))
        macd_trends = pd.DataFrame({"Dates": self.dt_dates_list, "Close": self.close.values,
                                    "MACD":MACD.values, "MACDsign":MACDsign.values, "MACDdiff":MACDdiff.values}, index=range(len(self.dt_dates_list)))
        return macd_trends.dropna()

