from trade_bots.generic_bots.predictive_trade_bot_v2 import PredictiveTradeBotV2
from data_loader.yahoo_stock_data_feed_v2 import YahooStockDataFeed
from trade_sim.bot_portfolio_v2 import Portfolio
from trading_strategies.basic_rsi_strategy import BasicRSIStrategy


class TradingSimulator:

	def __init__(self, trading_strategy, data_source, stock_symbols_list=None, trade_bots_num=None, trade_bots_list=None,
				 trade_bot_type=None):
		"""

		:param stock_symbols_list: a lst of stock symbols e.g. stock_data_settings["stock_symbols"] -> ["AAPL", "AMD", "INTC"]
		:param trade_bots_num: ant int value of the number of trading bots to generate to populate the trading/market simulation
		:param trading_strategy: a class obj of a certain trading strategy class (which inherits from
		the ABC AbstractBaseStrategy()) e.g. BasicRSIStrategy()
		:param data_source_obj: a class obj of a certain data source class (which inheirts from
		the ABC AbstractStockDataFeed ) e.g. YahooStockDataFeed(list_of_all_stock_symbols)
		"""

		self.trade_bots_list = trade_bots_list
		self.stock_symbols_list = stock_symbols_list
		self._set_sim_stock_symbols(stock_symbols_list)
		self.trade_bot_type = trade_bot_type
		# self.trade_bots_num = len(trade_bots_list) if trade_bots_num is None else trade_bots_num
		self.strategy = trading_strategy
		self.data_source = data_source
		self._stocks_market_data_dict()
		self._stocks_data_gens_dict()
		self.dates_idx = self.stocks_market_data_dict[self.stock_symbols_list[0]].index
		self.sim_portfolio = Portfolio()
		self.portfolios = []
		self._generate_bots()
		# self._bots_idx_key_dict()

		self.first_date = self.dates_idx[0]
		self.last_date = self.dates_idx[-1]

		self.current_date = None
		self.current_signal = None
		self.current_price = None

	def _set_sim_stock_symbols(self, stock_symbols_list):
		"""

		:param stock_symbols_list: a lst of stock symbols! If left as def val of None then the stocks symbols of each of the
		manual provided bots (via the trade_bots_list arg) will be collected.
		:return:
		"""
		bots_unique_stock_symbols_list = []
		if stock_symbols_list is None and self.trade_bots_list is not None:
			for bot_i in self.trade_bots_list:
				for bot_i_stock_i in bot_i.stock_symbols_list:
					if bot_i_stock_i not in bots_unique_stock_symbols_list:
						bots_unique_stock_symbols_list.append(bot_i_stock_i)
			self.stock_symbols_list = bots_unique_stock_symbols_list
		elif self.stock_symbols_list is not None and self.trade_bots_list is None:
			self.stock_symbols_list = stock_symbols_list

	def _stocks_market_data_dict(self):
		"""
		Creates the dict of stock symbol/stock pandas DataFrame key value pairs
		:return:
		"""
		self.data_source.stock_symbols_list = self.stock_symbols_list
		self.stocks_market_data_dict = self.data_source.stocks_market_data_dict

	def _stocks_data_gens_dict(self):
		"""
		creates a class instance attribute, stocks_data_gens_dict, which is assi    gned to a dict
		consisting of stock_symbols and stock pandas DataFrame generator objs key/value pairs.
		:return: None
		"""
		stocks_data_gens_dict = {}
		for stock_idx, stock_df in self.stocks_market_data_dict.items():
			stocks_data_gens_dict[stock_idx] = stock_df.iterrows()
		self.stocks_data_gens_dict = stocks_data_gens_dict

	def _bots_idx_key_dict(self):
		"""
		Creates a dict of int/bot class instance obj key/value pairs for convenience
		:return:
		"""
		bots_idx_dict = {}
		if self.trade_bots_list is not None:
			for bot_i_idx in range(len(self.trade_bots_list)):
				bots_idx_dict[bot_i_idx] = self.trade_bots_list[bot_i_idx]
			self.bots_idx_dict = bots_idx_dict
		elif self.trade_bots_list is None:
			pass

	def _bot_stocks_data_dict(self, bot_stock_symbols):
		pass


	def _generate_bots(self):
		print("\nChecking if trade bots have been provided...")
		if self.trade_bots_list is not None:
			print("\nTrading bots provided: {0}\nWith stock symbols: {1}".format(self.trade_bots_list, self.stock_symbols_list))
			pass
		elif self.trade_bots_list is None and self.stock_symbols_list is not None:
			print("No trade bots provided, stock symbols list provided instead: {0}".format(self.stock_symbols_list))
			print("Generating trading bot for each stock symbol: {0}".format(self.stock_symbols_list))
			generated_trade_bots_list = []
			generated_bots_stock_symbols_dict = {}
			if self.trade_bot_type is None:
				for stock_symbol_i_idx in range(len(self.stock_symbols_list)):
					print("Generating trade bot for stock symbol: {0}".format([self.stock_symbols_list[stock_symbol_i_idx]]))
					bot_i = PredictiveTradeBotV2(stock_symbol_i_idx, stock_symbols_list=[self.stock_symbols_list[stock_symbol_i_idx]])
					generated_bots_stock_symbols_dict[self.stock_symbols_list[stock_symbol_i_idx]] = bot_i
					generated_trade_bots_list.append(bot_i)
				self.trade_bots_list = generated_trade_bots_list
				self.generated_bots_stock_symbols_dict = generated_bots_stock_symbols_dict
			else:
				pass
		else:
			pass




if __name__ == "__main__":
	from configs_and_settings.settings import stock_data_settings
	stock_symbols_lst = stock_data_settings["stock_symbols"]
	# trade_bots_num = 2
	trading_strategy = BasicRSIStrategy()
	data_source1 = YahooStockDataFeed()
	data_source2 = YahooStockDataFeed()
	data_source3 = YahooStockDataFeed()

	stock_symbols = stock_data_settings["stock_symbols"]
	stock_symbols_list1 = ["INTC", "MSFT"]
	stock_symbols_list2 = ["TXN", "AMD"]
	stock_symbols_list3 = ['QCOM', 'XLNX']

	# ['INTC', 'NVDA', 'MU', 'QCOM', 'AMD', 'XLNX', 'ASML', 'TXN', 'AAPL']

	bot1 = PredictiveTradeBotV2(1, stock_symbols_list=stock_symbols_list1)
	bot2 = PredictiveTradeBotV2(2, stock_symbols_list=stock_symbols_list2)

	# trade_bots_lst = [bot1, bot2]

	sim1 = TradingSimulator(trading_strategy, data_source1, trade_bots_list=[bot1, bot2])
	sim2 = TradingSimulator(trading_strategy, data_source2, stock_symbols_list=["TXN", "AMD"])
	# print("sim1 stock_symbols_list: {0}".format(sim1.stock_symbols_list))
	# print("sim2 stock_symbols_list: {0}".format(sim2.stock_symbols_list))
	# sim3 = TradingSimulator(trading_strategy, data_source3, trade_bot_type=stock_symbols_list3)

