from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AbstractTradeBot(ABC):
	abc_name = "AbstractTradeBot"
	# init_cash_sum = 10000 # def val
	# current_cash_sum = 1000
	# current_investment_sum = 0
	# _bot_max_trade_risk_pct = 10
	
	@property
	def bot_type_name(self):
		raise NotImplementedError
	
	@abstractmethod
	def _set_bot_unique_id_and_name(self, unique_id):
		self.unique_id = unique_id
		self.name = "{0}{1}".format(self.bot_type_name, unique_id)
	
	# @abstractmethod
	def _set_init_cash_sum(self, init_cash_sum):
		self.init_cash_sum = init_cash_sum
	
	# @abstractmethod
	def _set_max_trade_risk_pct(self, max_trade_risk_pct):
		self.max_trade_risk_pct = max_trade_risk_pct
		
	# @abstractmethod
	def _set_sl_tp_pct_limits(self, sl_pct_limit, tp_pct_limit):
		self.sl_pct_limit = sl_pct_limit
		self.tp_pct_limit = tp_pct_limit
		
	def _set_trading_strategy(self, trading_strategy):
		self.trading_strategy = trading_strategy
		
	# @property
	# def stock_symbols(self):
	# 	raise NotImplementedError
	
	@abstractmethod
	def _create_portfolio(self, init_cash_sum, max_trade_risk_pct, sl_pct_limit, tp_pct_limit, trading_strategy):
		self._set_init_cash_sum(init_cash_sum)
		self._set_max_trade_risk_pct(max_trade_risk_pct)
		self._set_sl_tp_pct_limits(sl_pct_limit, tp_pct_limit)
		self._set_trading_strategy(trading_strategy)
		
	# @abstractmethod
	# def _get_stocks_data(self):
	# 	raise NotImplementedError
		
	# 	self.cash_balance = init_cash_sum
	# 	self.open_orders_current_tot_val = 0
	# 	self.tot_val = self.cash_balance + self.open_orders_current_tot_val
	# 	self.stock_idx_list = stock_idx_list
	# 	self.open_orders = []
	# 	self.closed_orders = []
	# 	pass

	@abstractmethod
	def trade(self):
		pass

	@property
	def net_balance(self):
		return self.current_cash_sum + self.current_investment_sum
