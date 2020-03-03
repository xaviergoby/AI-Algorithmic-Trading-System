from trade_bots.abc_bots.abstract_bot import AbstractTradeBot
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PredictiveTradeBot(AbstractTradeBot):
	
	bot_type_name = "PredictiveTradeBot"

	def __init__(self, stock_symbols, unique_id, init_cash_sum,
				 max_trade_risk_pct, sl_pct_limit, tp_pct_limit, trading_strategy, data_source):
		
		self.stock_symbols = stock_symbols
		# self.signal = signal
		self.unique_id = unique_id
		self.data_source = data_source
		# self.max_trade_risk_pct = max_trade_risk_pct
		# self.sl_pct_limit = sl_pct_limit
		# self.tp_pct_limit = tp_pct_limit
		self.all_stocks_symbols_data_dict = {}
		self.stocks_trading_strategy_signals_dict = {}
		
		self._set_bot_unique_id_and_name(unique_id)
		self._create_portfolio(init_cash_sum, max_trade_risk_pct, sl_pct_limit, tp_pct_limit, trading_strategy)
		self.generate_all_trading_strategy_signals()
		self.get_all_stocks_data()
		# self.signals_dict = self.stocks_trading_strategy_signals_dict
		# self.signals = self.trading_strategy.

		
	def _set_bot_unique_id_and_name(self, unique_id):
		super()._set_bot_unique_id_and_name(unique_id)
		
	def _create_portfolio(self, init_cash_sum, max_trade_risk_pct, sl_pct_limit, tp_pct_limit,
	                      trading_strategy):
		super()._create_portfolio(init_cash_sum, max_trade_risk_pct, sl_pct_limit, tp_pct_limit, trading_strategy)
		
	def get_all_stocks_data(self):
		for stock_symbol in list(self.data_source.stocks_market_data_dict.keys()):
			self.all_stocks_symbols_data_dict[stock_symbol] = self.data_source.stocks_market_data_dict[stock_symbol].head()
		
	def generate_all_trading_strategy_signals(self):
		for stock_symbol, stock_data in self.data_source.stocks_data_dict.items():
			sig = self.trading_strategy.generate_signal(stock_data).head()
			self.stocks_trading_strategy_signals_dict[stock_symbol] = sig

		
	# def _assign_bot_unique_id_and_name(self, unique_id):
	# 	super()._assign_bot_unique_id_and_name(unique_id)
	# 	self.name = "{0}{1}".format(self.bot_type_name, unique_id)

	def trade(self):
		pass
		# for time_step in range(len(self.signal)):
		#     logger.info("Current signal: {0}".format(time_step))
		#     if self.signal[time_step] == 0:
		#         print("Holding")
		#     elif self.signal[time_step] == 1:
		#         if -1 in self.signal[time_step:]:
		#             print("Buying")
		#             self.current_cash_sum = self.current_cash_sum - 100
		#             self.current_investment_sum = self.current_investment_sum + 100
		#         else:
		#             print("Holding")
		#     else:
		#         print("Selling")
		#         self.current_cash_sum = self.current_cash_sum + 200
		#         self.current_investment_sum = self.current_investment_sum - 100
		self.performance()

	def performance(self):
		print("{0} final cash sum (not incl. value of remaining open orders): {1}".format(self.bot_type_name, self.current_cash_sum))
		
if __name__ == "__main__":
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

	
	trading_strategy1 = BasicRSIStrategy()
	trading_strategy2 = BasicRSIStrategy()
	# trading_strategy2 = BasicRFCStrategy()
	# trading_strategy2 = BasicRFCStrategy(data2)
	# ['INTC', 'NVDA', 'MU', 'QCOM', 'AMD', 'XLNX', 'ASML', 'TXN', 'AAPL']
	
	
	bot1 = PredictiveTradeBot(stockslist1, 1, 100, 15, 10, 10, trading_strategy1, data_source1)
	bot2 = PredictiveTradeBot(stockslist2, 2, 100000, 5, 5, 5, trading_strategy2, data_source2)
	
	print("\n***** TEST OUTPUT ***** TEST OUTPUT ***** TEST OUTPUT *****\n")
	print("bot1 unique_id: {0} and bot2 unique_id: {1}".format(bot1.unique_id, bot2.unique_id))
	print("bot1 name: {0} and bot2 name: {1}".format(bot1.name, bot2.name))
	print("bot1 init_cash_sum: {0} and bot2 init_cash_sum: {1}".format(bot1.init_cash_sum, bot2.init_cash_sum))
	print("bot1 tp_pct_limit: {0} and bot2 tp_pct_limit: {1}".format(bot1.tp_pct_limit, bot2.tp_pct_limit))
	print("bot1 sl_pct_limit: {0} and bot2 sl_pct_limit: {1}".format(bot1.sl_pct_limit, bot2.sl_pct_limit))
	print("bot1 trading_strategy.name: {0} and bot2 trading_strategy.name: {1}".format(bot1.trading_strategy.name, bot2.trading_strategy.name))
	# print("bot1 trading_strategy.signal: {0} and bot2 trading_strategy.signal: {1}".format(bot1.trading_strategy.signal.head(), bot2.trading_strategy.signal))
	# print("bot1 trading_strategy.signal: {0} and bot2 trading_strategy.signal: {1}".format(bot1.stocks_trading_strategy_signals_dict[stock11].head(),
	#                                                                                        bot2.stocks_trading_strategy_signals_dict[stock21].head()))
	
	print("\n***** TEST OUTPUT ***** TEST OUTPUT ***** TEST OUTPUT *****")
	
	
