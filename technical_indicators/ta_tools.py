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
	# def rsi(stock_data_df, stock_symbol, period=14):
	def rsi(stock_data_df, period=14.0):
		"""
		STATUS: VERIFIED (with Investing.com) on NVDA between 10-06-2019 & 14-06-2019
		If rsi > 70: Overbought - (Strong Sell Signal)
		If rsi < 30: Oversold - (Strong Buy Signal)
		:param stock_data_df: The original OHCLV and VWAP pandas DataFrame output of i.e. the data_loader.data_sources.get_stocks_data()
		:param stock_symbol: str of the stock symbol
		:param period: Int of the number of days in the time period for computing the trend line values. Is 14 by def
		:return: A pandas Series w/ index=DatetimeIndex & name (so Series_data_returned.name):
		"stock_symbol"_rsi_"period"
		"""
		# feature_name = "{0}_rsi_{1}d".format(stock_symbol, period)
		delta = stock_data_df["Close"].diff()
		up, down = delta.copy(), delta.copy()

		up[up < 0] = 0
		down[down > 0] = 0

		roll_up = up.ewm(com=period - 1, adjust=False).mean()
		roll_down = down.ewm(com=period - 1, adjust=False).mean().abs()

		rsi = 100 - 100 / (1 + roll_up / roll_down)

		# rsi.name = feature_name
		rsi = rsi.dropna()
		return rsi


	@staticmethod
	def macd(stock_data_df, stock_symbol, fast_ma_period = 12, slow_ma_period = 26, signal_line_period = 9):
		"""
		# long-term trend <==> slow_ma_period, 26 typically days and by def
		# short-term trend <==> fast_ma_period, 12 typically days and by def
		:param stock_data_df: pandas.DataFrame
		:param fast_ma_period: int of short-term trend moving average period days duration, 12 by def
		:param slow_ma_period: int of long-term trend moving average period days duration, 26 by def
		:param signal_line_period: int of cross-over signal line moving average period days duration, 9 by def
		:return: pandas.DataFrame
		"""
		pd_dt_idx = stock_data_df.index
		EMAfast = pd.Series(stock_data_df['Close'].ewm(span=fast_ma_period, min_periods=slow_ma_period).mean())
		EMAslow = pd.Series(stock_data_df['Close'].ewm(span=slow_ma_period, min_periods=slow_ma_period).mean())
		MACD = pd.Series(EMAfast - EMAslow, name='MACD_' + str(fast_ma_period) + '_' + str(slow_ma_period))
		# MACDsign = pd.Series(MACD.ewm(span=signal_line_period).mean(), name='MACDsign_' + str(fast_ma_period) + '_' + str(slow_ma_period))
		# MACDsign = pd.Series(MACD.ewm(span=signal_line_period, min_periods=signal_line_period).mean(), name='MACDsign_' + str(fast_ma_period) + '_' + str(slow_ma_period))
		# MACDsign = pd.Series(MACD.ewm(span=signal_line_period).mean(), name="SIGNAL")
		MACDsign = pd.Series(MACD.ewm(ignore_na=False, min_periods=0, com=signal_line_period - 1, adjust=True).mean(), name="SIGNAL")
		# MACDdiff = pd.Series(MACD - MACDsign, name='MACDdiff_' + str(fast_ma_period) + '_' + str(slow_ma_period))
		# macd_data = pd.DataFrame({"MACD":MACD, "MACDsign":MACDsign, "MACDdiff":MACDdiff}, index=pd_dt_idx)
		macd_data = pd.DataFrame({"MACD":MACD, "MACDsign":MACDsign}, index=pd_dt_idx)
		# stock_data_df = stock_data_df.join(MACD)
		# stock_data_df = stock_data_df.join(MACDsign)
		# stock_data_df = stock_data_df.join(MACDdiff)
		return macd_data


if __name__ == "__main__":
	from configs_and_settings.settings import stock_data_settings
	from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
	stock_symbols = stock_data_settings["stock_symbols"]
	stock_symbol = "NVDA"
	stock_data = YahooStockDataFeed(stock_symbols).stocks_data_dict[stock_symbol]
	rsi = TATools().rsi(stock_data)
	print(stock_data.head())
	print(rsi.head())
	print(len(stock_data))
	print(len(rsi))
	# import matplotlib.pyplot as plt
	# rsi.plot()
	# rsi.plot().plot_date(rsi)
	# rsi.plot_date()
	# plt.show()
