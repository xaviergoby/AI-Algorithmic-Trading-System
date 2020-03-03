from trade_sim.market_order import Order
import pandas as pd

class BotPortfolio:

	def __init__(self, init_cash_sum=1000, tp_limit=10, sl_limit=10, max_trade_risk_pct=50):
		self.init_cash_sum = init_cash_sum
		self.tp_limit = tp_limit
		self.sl_limit = sl_limit
		self.max_trade_risk_pct = max_trade_risk_pct