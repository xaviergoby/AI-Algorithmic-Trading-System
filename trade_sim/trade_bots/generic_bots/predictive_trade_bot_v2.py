from trade_sim.trade_bots.generic_bots.generic_bot import GenericBot

class PredictiveTradeBotV2(GenericBot):
	bot_type_name = "PredictiveTradeBotV2"

	def __init__(self, unique_id, **kwargs):
		super().__init__(unique_id, **kwargs)


if __name__ == "__main__":
	stock_symbols_list1 = ["AAPL", "AMD"]
	stock_symbols_list2 = ["NVDA", "TXN"]
	stock_symbols_list3 = ["QCOM", "XLNX"]
	bot1 = PredictiveTradeBotV2(1, stock_symbols_list=stock_symbols_list1)
	bot2 = PredictiveTradeBotV2(2, stock_symbols_list=stock_symbols_list2,
	                            init_cash_sum = 99999, sl_limit=2)
	bot3 = PredictiveTradeBotV2(3, stock_symbols_list=stock_symbols_list3)
	bot4 = PredictiveTradeBotV2(4)
	bot1.print_bot_settings()
	bot2.print_bot_settings()
	bot3.print_bot_settings()
	bot4.print_bot_settings()
	# print(bot1.init_cash_sum)
	# print(bot1.stock_symbols_list)
	# print(bot2.init_cash_sum)
	# print(bot2.stock_symbols_list)