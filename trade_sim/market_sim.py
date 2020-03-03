from trade_bots.abc_bots.predictive_trade_bot import PredictiveTradeBot
from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
from trade_sim.bot_portfolio import Portfolio
from configs_and_settings.settings import stock_data_settings
from trading_strategies.basic_rsi_strategy import BasicRSIStrategy




class TradingSimulator:

	def __init__(self, stock_symbols_list, trading_strategy, data_source_obj, trade_bots_num = None, trade_bots_list = None):
		"""
		
		:param stock_symbols_list: a lst of stock symbols e.g. stock_data_settings["stock_symbols"] -> ["AAPL", "AMD", "INTC"]
		:param trade_bots_num: ant int value of the number of trading bots to generate to populate the trading/market simulation
		:param trading_strategy: a class obj of a certain trading strategy class (which inherits from
		the ABC AbstractBaseStrategy()) e.g. BasicRSIStrategy()
		:param data_source_obj: a class obj of a certain data source class (which inheirts from
		the ABC AbstractStockDataFeed ) e.g. YahooStockDataFeed(list_of_all_stock_symbols)
		"""
		self.stock_symbols = stock_symbols_list
		self.trade_bots_list = trade_bots_list
		self.trade_bots_num = len(trade_bots_list) if trade_bots_num is None else trade_bots_num
		self.trade_bots_list = trade_bots_list
		self.strategy = trading_strategy
		self.data_source_obj = data_source_obj
		self.stocks_market_data_dict = self.data_source_obj.stocks_data_dict
		self.dates_idx = self.stocks_market_data_dict[self.stock_symbols[0]].index
		self._stocks_data_gens_dict()
		self.sim_portfolio = Portfolio()
		self.portfolios = []
		self.bots_idx_dict = {}
		self._generate_trade_bots()
		
		self.first_date = self.dates_idx[0]
		self.last_date = self.dates_idx[-1]

		self.current_date = None
		self.current_signal = None
		self.current_price = None

	def _stocks_data_gens_dict(self):
		"""
		creates a class instance attribute, stocks_data_gens_dict, which is assi    gned to a dict
		consisting of stock_symbols and stock pandas DataFrame generator objs key/value pairs.
		:return: None
		"""
		self.stocks_data_gens_dict = {}
		for stock_idx, stock_df in self.stocks_market_data_dict.items():
			self.stocks_data_gens_dict[stock_idx] = stock_df.iterrows()
			
	def single_stock_bot_sim(self):
		num_of_bots = self.trade_bots_num
		for bot_i in range(num_of_bots+1):
			pass
		
			
	
			
	def _generate_trade_bots(self, all_stock_symbols = True):
		for i in range(1, self.trade_bots_num + 1):
			if all_stock_symbols is True:
				trade_bot_i = PredictiveTradeBot(self.stock_symbols, i, 1000, 50, 10, 10, self.strategy, self.data_source_obj)
				self.bots_idx_dict[i] = trade_bot_i
			# self.bots_dict[] =
			# pass
	
	def init_market_sim(self, ):
		if self.current_date is None:
			self.current_date = self.first_date
		else:
			pass
		if self.trade_bots_list is not None:
			for i in self.trade_bots_list:
				# trade_bot_i = PredictiveTradeBot(self.stock_symbols, i, init_cash_sum, max_trade_risk_pct, 10, 10,
				#                                  self.strategy, self.data_source_obj)
				self.bots_idx_dict[i.unique_id] = i
		elif self.trade_bots_list is None:
			self._generate_trade_bots()
		
	def update_market_sim(self, current_date_idx):
		pass
		self.current_date = current_date_idx
		
	def run_market_sim(self, first_date = None, last_date = None):
		if first_date is None and last_date is None:
			# pass
			self.current_date_idx = 0
			first_date = self.dates_idx[0]
			last_date = self.dates_idx[-1]
			self.current_date = self.dates_idx[current_date_idx]
		else:
			pass
		while self.current_date is not last_date:
			
			pass
			
	
	
		

	def get_next_bar(self):
		# stock_data_df = self.get_market_data()
		# for index, row in stock_data_df.iterrows():
		x = 0
		# for bar in stock_data_df.iterrows():
		# df_gen = self.stock_data_df.iterrows()
		# yield next(stock_data_df)
		# return next(df_gen)
			# if x != 3:
			#     x = x + 1
			#     yield bar
			# else:
			#     print("x=3")
		pass


	def run_sim(self):
		pass


	# def run_sim(self):
	#
	#     stock_data = self.data_source.stocks_data_dict["NVDA"].tail(100)
	#
	#     self.strategy.generate_signal(stock_data)
	#
	#     for bar in self.strategy.signal.iteritems():
	#
	#         self.current_date = bar[0]
	#         self.current_signal = bar[1]
	#         self.current_price = stock_data["Close"].loc[self.current_date]
	#         print("\nCurrent date: {0}\nCurrent signal: {1}\nCurrent Close Price: {2}".format(
	#             self.current_date, self.current_signal, self.current_price
	#         ))
	#         self.portfolio.update_portfolio(self.current_date, self.current_price) # 1
	#
	#         if self.current_signal == 1:
	#             # print("Signal: 1  on Date: {0}".format(self.current_date))
	#             self.portfolio.long_position_consultant()
	#         #
	#         elif self.current_signal == -1 or self.current_signal == 0:
	#             pass
	#
	#         print("Current cash balance: ", self.portfolio.cash_balance)
	#         print("Current portfolio value: ", self.portfolio.current_portfolio_value)


if __name__ == "__main__":

	stock_symbols_list = stock_data_settings["stock_symbols"]
	trade_bots_num = 2
	trading_strategy = BasicRSIStrategy()
	data_source = YahooStockDataFeed(stock_symbols_list)

	
	from trading_strategies.basic_rsi_strategy import BasicRSIStrategy
	from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
	from configs_and_settings.settings import stock_data_settings
	
	stock_symbols = stock_data_settings["stock_symbols"]
	stockslist1 = ["INTC", "AAPL"]
	stockslist2 = ["TXN", "AMD"]
	stock11 = stockslist1[0]
	stock21 = stockslist2[0]
	data_source1 = YahooStockDataFeed(stockslist1)
	data_source2 = YahooStockDataFeed(stockslist2)
	
	# trading_strategy1 = BasicRSIStrategy()
	# trading_strategy2 = BasicRSIStrategy()
	# trading_strategy2 = BasicRFCStrategy()
	# trading_strategy2 = BasicRFCStrategy(data2)
	# ['INTC', 'NVDA', 'MU', 'QCOM', 'AMD', 'XLNX', 'ASML', 'TXN', 'AAPL']
	
	
	# __init__(self, stock_symbols_list, trading_strategy, data_source_obj, trade_bots_num = None, trade_bots_list = None):
	bot1 = PredictiveTradeBot(stockslist1, 1, 100, 15, 10, 10, trading_strategy, data_source)
	bot2 = PredictiveTradeBot(stockslist2, 2, 100000, 5, 5, 5, trading_strategy, data_source)
	
	trade_bots_list = [bot1, bot2]
	
	sim = TradingSimulator(stock_symbols_list, trading_strategy, data_source, trade_bots_list = trade_bots_list)
	
	print("\n***** TEST OUTPUT ***** TEST OUTPUT ***** TEST OUTPUT *****\n")
	print("bot1 unique_id: {0} and bot2 unique_id: {1}".format(bot1.unique_id, bot2.unique_id))
	print("bot1 name: {0} and bot2 name: {1}".format(bot1.name, bot2.name))
	print("bot1 init_cash_sum: {0} and bot2 init_cash_sum: {1}".format(bot1.init_cash_sum, bot2.init_cash_sum))
	print("bot1 tp_pct_limit: {0} and bot2 tp_pct_limit: {1}".format(bot1.tp_pct_limit, bot2.tp_pct_limit))
	print("bot1 sl_pct_limit: {0} and bot2 sl_pct_limit: {1}".format(bot1.sl_pct_limit, bot2.sl_pct_limit))
	print("bot1 trading_strategy.name: {0} and bot2 trading_strategy.name: {1}".format(bot1.trading_strategy.name,
	                                                                                   bot2.trading_strategy.name))
	# print("bot1 trading_strategy.signal: {0} and bot2 trading_strategy.signal: {1}".format(bot1.trading_strategy.signal.head(), bot2.trading_strategy.signal))
	# print("bot1 trading_strategy.signal: {0} and bot2 trading_strategy.signal: {1}".format(bot1.stocks_trading_strategy_signals_dict[stock11].head(),
	#                                                                                        bot2.stocks_trading_strategy_signals_dict[stock21].head()))
	
	print("\n***** TEST OUTPUT ***** TEST OUTPUT ***** TEST OUTPUT *****")
	