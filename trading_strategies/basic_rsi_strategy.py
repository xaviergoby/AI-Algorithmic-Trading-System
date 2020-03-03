from trading_strategies.abstract_base_strategy import AbstractBaseStrategy
from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
from technical_indicators.ta_tools import TATools


class BasicRSIStrategy(AbstractBaseStrategy):
	
	name = "BasicRSIStrategy"

	# def __init__(self, data, over_bought_level=70, over_sold_level=30, period=14, signal=None):
	def __init__(self, over_bought_level=70, over_sold_level=30, period=14):
		"""
		:param data: a pandas DataFrame of the stock OHCLV & Adj. Close data
		:param over_bought_level: int of the over bought level, is 70 by def
		:param over_sold_level: int of the over sold level, is 30 by def
		:param period: int of the time period, is 14 by def
		:param signal: a pandas Series of a specific signal which can be optionally used as opposed
		to computing/generating one. If left unchanged (so left as None as by default) then a signal
		will be generated upon the time of class initialisation
		"""
		# self.data = data
		self.over_bought_level = over_bought_level
		self.over_sold_level = over_sold_level
		self.period = period
		# self.signal = signal
		# self._generate_signal()

	def generate_signal(self, data):
		# if self.signal is None:
		rsi = TATools().rsi(data, period=self.period)
		rsi_nonan = rsi.dropna()
		rsi_nonan_copy = rsi_nonan.copy()
		rsi_nonan_copy[rsi_nonan_copy < self.over_sold_level] = 1
		rsi_nonan_copy[rsi_nonan_copy > self.over_bought_level] = -1
		rsi_nonan_copy[(rsi_nonan_copy > self.over_sold_level) & (rsi_nonan_copy < self.over_bought_level)] = 0
		self.signal = rsi_nonan_copy
		return self.signal
		# else:
		# pass


if __name__ == "__main__":
	from configs_and_settings.settings import stock_data_settings
	stock_symbols = stock_data_settings["stock_symbols"]
	data1 = YahooStockDataFeed(stock_symbols).stocks_data_dict["NVDA"]
	data2 = YahooStockDataFeed(stock_symbols).stocks_data_dict["AAPL"]
	data3 = YahooStockDataFeed(stock_symbols).stocks_data_dict["AMD"]
	s1 = BasicRSIStrategy(data1)
	rsi1 = s1.signal
	s2 = BasicRSIStrategy(data2)
	rsi2 = s2.signal
	s3 = BasicRSIStrategy(data3, signal = rsi1)
	rsi3 = s3.signal



