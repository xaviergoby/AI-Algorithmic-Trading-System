import numpy as np
import pandas as pd

class SMACrossOver:

    def __init__(self, close, short_trend_period=42, long_trend_period=252, threshold=5):
        # 1
        self.close = close
        # 2
        self._short_trend_period = short_trend_period
        self._long_trend_period = long_trend_period
        self._threshold = threshold
        # 3
        self.sma_crossover_values = self.get_sma_crossover_values()
        # 4
        self.sma_crossover_labels = self.get_sma_crossover_labels()

    def get_sma_crossover_values(self):
        short_sma = np.round(self.close.rolling(window=self._short_trend_period).mean(), 4)
        long_sma = np.round(self.close.rolling(window=self._long_trend_period).mean(), 4)
        sma_crossover_diff = short_sma - long_sma
        sma_crossover_diff = sma_crossover_diff
        sma_crossover_diff = sma_crossover_diff.dropna()
        sma_crossover_diff.rename("SMACrossOver")
        return sma_crossover_diff

    def get_sma_crossover_labels(self):
        sma_crossover_labels_list = []
        signal = self.get_sma_crossover_values().dropna().values
        for s in signal:
            if s > self._threshold:
                sma_crossover_labels_list.append("Buy")
            elif s <= -self._threshold:
                sma_crossover_labels_list.append("Sell")
            else:
                sma_crossover_labels_list.append("Hold")
        sma_series = pd.Series
        return sma_crossover_labels_list

    def get_sma_crossover_int_labels(self):
        sma_crossover_labels_list = []
        signal = self.get_sma_crossover_values().dropna().values
        for s in signal:
            if s > self._threshold:
                sma_crossover_labels_list.append(1)
            elif s <= -self._threshold:
                sma_crossover_labels_list.append(-1)
            else:
                sma_crossover_labels_list.append(0)
        sma_series = pd.Series
        return sma_crossover_labels_list





