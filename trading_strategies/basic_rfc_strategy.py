from trading_strategies.abstract_base_strategy import AbstractBaseStrategy
from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
from technical_indicators.ta_tools import TATools


class BasicRFCStrategy(AbstractBaseStrategy):
	name = "BasicRFCStrategy"
	
	# def __init__(self, data, signal=None):
	def __init__(self, signal=None):
		"""
		:param data: a pandas DataFrame of the stock OHCLV & Adj. Close data
		:param signal: a pandas Series of a specific signal which can be optionally used as opposed
		to computing/generating one. If left unchanged (so left as None as by default) then a signal
		will be generated upon the time of class initialisation
		"""
		# self.data = data
		self.signal = signal
		# self._generate_signal()
	
	def generate_signal(self, data):
		if self.signal is None:
			return self.signal
			# return 0
		else:
			return self.signal
			# return 0


if __name__ == "__main__":
	from configs_and_settings.settings import stock_data_settings
	
	stock_symbols = stock_data_settings["stock_symbols"]




