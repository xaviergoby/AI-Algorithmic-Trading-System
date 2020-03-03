from trade_sim.bot_portfolio_v2 import Portfolio


class GenericBot:

	def __init__(self, unique_id, **kwargs):
		self.unique_id = unique_id
		self.portfolio = Portfolio(**kwargs)

	@property
	def stock_symbols_list(self):
		return self.portfolio.stock_symbols_list

	def print_bot_settings(self):
		print("Bot settings:\nInitial cash sum: {0}\nStop loss limit: {1}\nTake profit limit: {2}"
		      "\nMax trade risk pct: {3}\nStock symbols: {4}".format(self.portfolio.init_cash_sum,
		                                                             self.portfolio.sl_limit,
		                                                             self.portfolio.tp_limit,
		                                                             self.portfolio.max_trade_risk_pct,
		                                                             self.portfolio.stock_symbols_list))

	# def _create_portfolio(self):
		# self.portfolio = Portfolio(stock_symbols_list=self.stock_symbols_list, init_cash_sum=self.init_cash_sum,
		#                            sl_limit=self.sl_limit, tp_limit=self.tp_limit,
		#                            max_trade_risk_pct=self.max_trade_risk_pct)
		# self.portfolio = Portfolio(kwargs)

	# @property
	# def stock_symbols_list(self):
	# 	self.portfolio