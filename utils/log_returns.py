import numpy as np
import pandas as pd

def get_log_returns(data):
	log_returns = np.log(data / data.shift(1))


if __name__ == "__main__":
	from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
	from configs_and_settings.settings import stock_data_settings
	stock_symbols = stock_data_settings["stock_symbols"]
	src = YahooStockDataFeed(stock_symbols)
	stock_symbol = "NVDA"
	stock_data = src.stocks_data_dict[stock_symbol]
	data = stock_data.Close
	print(data)
