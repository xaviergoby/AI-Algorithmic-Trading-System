from trade_bots.abc_bots.abstract_bot import AbstractTradeBot
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClassicalTradeBot(AbstractTradeBot):

	bot_type_name = "ClassicalTradeBot"

	def __init__(self, stock_symbols, signal, unique_id):
		self.stock_symbols = stock_symbols
		self.signal = signal
		self._assign_bot_unique_id_and_name(unique_id)
		
	def _assign_bot_unique_id_and_name(self, unique_id):
		super()._assign_bot_unique_id_and_name(unique_id)
		self.name = "{0}{1}".format(self.bot_type_name, unique_id)
		
		
		
	# def __init__(self, data_source, portfolio, strategy):
		"""

		:param stock_symbols:
		:param strategy: a strategy class e.g. BasicRSIStrategy
		:param signal:
		"""
		# super().__init__(self, data_source, portfolio, strategy)
		# TradingSimulator.__init__(self, data_source, portfolio, strategy)
		# self.data_source = data_source
		# self.portfolio = portfolio
		# self.strategy = strategy
		# super.__init__(data_source, portfolio, strategy)


	def trade(self):
		for time_step in range(len(self.signal)):
			logger.info("Current signal: {0}".format(time_step))
			if self.signal[time_step] == 0:
				print("Holding")
			elif self.signal[time_step] == 1:
				print("Buying")
				self.current_cash_sum = self.current_cash_sum - 100
				self.current_investment_sum = self.current_investment_sum + 100
			else:
				print("Selling")
				self.current_cash_sum = self.current_cash_sum + 200
				self.current_investment_sum = self.current_investment_sum - 100
		self.performance()


	def performance(self):
		print("{0} final cash sum (not incl. value of remaining open orders): {1}".format(self.bot_type_name, self.current_cash_sum))