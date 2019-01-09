import pandas as pd
from revamp import new_sma_crossover
from technical_indicators.technical_indicator_funcs import SMA
from revamp import new_rsi
from load_data import data_getter_funcs


class ConstructSignal():

    def __init__(self, data):
        self.data = data
        self.dates = data.Dates.tolist()
        self.close = data.Close
        self.sma_crossover_signal = new_sma_crossover.SMACrossOver(self.close)
        self.rsi_signal = new_rsi.RSI(self.close)
        self.num_signals = []
        self.cat_signals = {}
        self.int_cat_signals = {}

    def compute_and_get_sma_crossover_signal_values(self, short_trend_period, long_trend_period):
        self.sma_crossover_signal._short_trend_period = short_trend_period
        self.sma_crossover_signal._long_trend_period = long_trend_period
        sma_crossover_signal_values = self.sma_crossover_signal.get_sma_crossover_values().dropna()
        self.num_signals.append(sma_crossover_signal_values)
        return sma_crossover_signal_values

    def get_sma_crossover_signal_labels(self, threshold):
        self.sma_crossover_signal._threshold = threshold
        sma_crossover_labels = self.sma_crossover_signal.get_sma_crossover_labels()
        self.cat_signals["SMACrossover"] = pd.Series(sma_crossover_labels).dropna()
        return sma_crossover_labels

    def get_sma_crossover_signal_int_labels(self, threshold):
        self.sma_crossover_signal._threshold = threshold
        sma_crossover_labels = self.sma_crossover_signal.get_sma_crossover_int_labels()
        self.int_cat_signals["SMACrossover"] = pd.Series(sma_crossover_labels).dropna()
        return sma_crossover_labels

    def compute_and_get_rsi_signal_values(self, time_period):
        self.rsi_signal._time_period = time_period
        rsi_signal_values = self.rsi_signal.get_rsi_values().dropna()
        self.num_signals.append(rsi_signal_values)
        return rsi_signal_values

    def get_rsi_signal_labels(self, overbought_level, oversold_level):
        self.rsi_signal._overbought_level = overbought_level
        self.rsi_signal._oversold_level = oversold_level
        rsi_signal_labels = self.rsi_signal.get_rsi_labels()
        self.cat_signals["RSI"] = pd.Series(rsi_signal_labels).dropna()
        return rsi_signal_labels

    def get_rsi_signal_int_labels(self, overbought_level, oversold_level):
        self.rsi_signal._overbought_level = overbought_level
        self.rsi_signal._oversold_level = oversold_level
        rsi_signal_labels = self.rsi_signal.get_rsi_int_labels()
        self.int_cat_signals["RSI"] = pd.Series(rsi_signal_labels).dropna()
        return rsi_signal_labels



    def combined_num_signals_into_df(self):
        df = pd.concat(self.num_signals, axis=1)
        return df.dropna()

    def combined_cat_signals_into_df(self):
        df = pd.concat(self.cat_signals, axis=1)
        df = df.dropna()
        df.index = self.combined_num_signals_into_df().index
        return df

    def combined_int_cat_signals_into_df(self):
        df = pd.concat(self.int_cat_signals, axis=1)
        df = df.dropna()
        df.index = self.combined_num_signals_into_df().index
        return df



# if __name__ == "__main__":
#     apple = data_getter_funcs.get_stocks_data()
#     strategy = SimpleBuyAndHoldStrategy(apple)
#
#     strategy_rsi_values = strategy.compute_and_get_rsi_signal_values(time_period=14)
#     strategy_rsi_labels = strategy.get_rsi_signal_labels(overbought_level=70, oversold_level=30)
#
#     strategy_sma_crossover_values = strategy.compute_and_get_sma_crossover_signal_values(short_trend_period=21, long_trend_period=42)
#     strategy_sma_crossover_labels = strategy.get_sma_crossover_signal_labels(threshold=3)
#
#     nums = strategy.combined_num_signals_into_df()
#     cats = strategy.combined_cat_signals_into_df()
#
#     # close = apple.Close
#     # print(close.head())
#     # nums.insert(0, "Close", close)
#     # print(nums.head())
#
#     close_change = apple.Close.diff()
#     print(close_change.tail())
#     nums.insert(0, "CloseChangeValues", close_change)
#     print(nums.tail())
#
#     up_down_labels = []
#
#     for d in nums["CloseChangeValues"].tolist():
#         if d < 0:
#             up_down_labels.append("Down")
#         else:
#             up_down_labels.append("Up")
#     cats.insert(0, "CloseChangeLabels", up_down_labels)
#
#     print(cats.tail())
#     print(nums.tail())
#
#     print(cats["RSI"].value_counts())
#     print(cats["SMACrossover"].value_counts())
#
#     samples_num = len(cats)
#     print("Number of total rows/bars/observations: {0}".format(samples_num))
#     train_size = int(samples_num * 0.7)
#     test_size = samples_num - train_size
#     train = cats[:train_size]
#     test = cats[train_size:]
#     print(len(train)+len(test) == samples_num)





