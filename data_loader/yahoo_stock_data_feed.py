import pandas_datareader as web
import pandas as pd
from data_loader.abstract_stock_data_feeder_class import AbstractStockDataFeed
from configs_and_settings.settings import default_settings
from datetime import datetime
import os
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class YahooStockDataFeed(AbstractStockDataFeed):
	name = "YahooStockDataFeed"
	source = "yahoo"

	def __init__(self, stock_symbols):
		self.stock_symbols = stock_symbols
		self.stocks_data_dict = self.load_basket_of_stocks_data_dict()
		# self._stocks_data_dict = self.load_basket_of_stocks_data_dict()
		# self.basket_of_stocks_data_dict = self.get_basket_of_stocks_data()
		# self.continue_backtest = True
		# self._current_new_bar = None
		# pass

	@property
	def stocks_market_data_dict(self):
		stock_market_data_dict = self.load_basket_of_stocks_data_dict()
		return stock_market_data_dict

	def get_stored_data_stock_symbols(self):
		file_names = os.listdir(os.path.abspath(self.data_dir_path))
		file_names_with_ext = [filename for filename in file_names if filename.endswith(".csv")]
		present_stock_csv_files = [stock_symbol.split('.')[0] for stock_symbol in file_names_with_ext]
		return present_stock_csv_files

	def compare_present_and_missing_stock_data(self):
		present_stock_data_symbols = self.get_stored_data_stock_symbols()
		missing_stock_symbols = []
		for stock_symbol in self.stock_symbols:
			if stock_symbol not in present_stock_data_symbols:
				missing_stock_symbols.append(stock_symbol)
		if len(missing_stock_symbols) == 0:
			return None
		else:
			return missing_stock_symbols

	def get_date_today(self):
		yahoo_fin_date_format = default_settings["yahoo_fin_time_format_str"]
		yahoo_fin_format_date_today = datetime.today().strftime(yahoo_fin_date_format)
		return yahoo_fin_format_date_today

	def get_stock_data(self, stock_symbol):
		stock_data = web.DataReader(stock_symbol, data_source=self.source, start=self.start_date, end=self.end_date)
		return stock_data
		# os.environ["IEX_API_KEY"] = "pk_960e75eef25a40eb960a43626ac4487a"

	def save_stock_data(self, stock_symbol, stock_data_df):
		# stock_data_csv_name = "{0}_{1}_{2}.csv".format(stock_symbol, self.start_date, self.end_date)
		stock_data_csv_name = "{0}.csv".format(stock_symbol)
		stock_data_csv_full_path = os.path.join(os.path.abspath(self.data_dir_path), stock_data_csv_name)
		stock_data_df.to_csv(stock_data_csv_full_path) # //TODO
		# stock_data_df.to_csv(stock_data_csv_full_path, index_label=[])

	def download_basket_of_stocks_data(self):
		stocks_dict = {}
		for stock_symbol in self.stock_symbols:
			stock_data = self.get_stock_data(stock_symbol)
			self.save_stock_data(stock_symbol, stock_data)
			# stocks_dict[stock_symbol] = stock_data
		# return stocks_dict

	def load_basket_of_stocks_df(self, stock_symbol):
		# stock_data_csv_name = "{0}_{1}_{2}.csv".format(stock_symbol, self.start_date, self.end_date)
		stock_data_csv_name = "{0}.csv".format(stock_symbol)
		stock_data_csv_full_path = os.path.join(os.path.abspath(self.data_dir_path), stock_data_csv_name)
		# stock_data_df = pd.read_csv(stock_data_csv_full_path, ) # //TODO
		stock_data_df = pd.read_csv(stock_data_csv_full_path, index_col=0, parse_dates=True) # //TODO
		return stock_data_df


	def load_basket_of_stocks_data_dict(self):
		if self.compare_present_and_missing_stock_data() is not None:
			self.download_basket_of_stocks_data()
		stocks_dict = {}
		for stock_symbol in self.stock_symbols:
			stock_data_df = self.load_basket_of_stocks_df(stock_symbol)
			stocks_dict[stock_symbol] = stock_data_df
		return stocks_dict

	def save_data(self):
		pass

	# def _get_new_bar(self, stock_symbol):
	#     # for row_index, row in self.stocks_data_dict[stock_symbol].iterrows():
	#     new_bar_tuple = self.stocks_data_dict[stock_symbol].iterrows()
	#     return new_bar_tuple
	#         # return row_index, row
	#
	# def update_stock_symbol_bar(self, stock_symbol):
	#     # if self._current_new_bar is None:
	#     #     self._current_new_bar = self._get_new_bar(stock_symbol)
	#     # else:
	#     #     return next(self._current_new_bar)
	#     #     return next(self._get_new_bar(stock_symbol))
	#         for b in self._get_new_bar(stock_symbol):
	#             yield b
	#
	# @property
	# def get_stocks_data_dict(self):
	#     return self._stocks_data_dict



if __name__ == "__main__":
	from configs_and_settings.settings import stock_data_settings
	import numpy as np


	stock_symbols = stock_data_settings["stock_symbols"]
	y = YahooStockDataFeed(stock_symbols)
	stock_symbol = "NVDA"
	x = y.stocks_data_dict[stock_symbol]
	data = x.Close
	means = []
	Sts = []
	start = 0
	ret = 0
	hits = {"dates":[], "price":[], "Sti":[]}
	for i in range(len(data.values)):
		print("\n")
		print(data.values[i])
		if i is not 0:
			St_i_min_1 = Sts[i-1]
			true_minus_mean = data.values[i] - mean
			Sti = max(0, St_i_min_1 + true_minus_mean)
			if Sti >= 10:
				hits["dates"].append(data.index[i])
				hits["price"].append(data.values[i])
				hits["Sti"].append(Sti)
				ret = ret + (5*data.values[i] - 5*data.values[start])
				# mean = 0
				# means.append(mean)
				Sti = 0
				start = i
			# else:
			# 	hits["dates"].append(data.index[i])
			# 	hits["price"].append(0)
			# 	hits["Sti"].append(Sti)
			Sts.append(Sti)
		elif i is 0:
			Sts.append(0)
		# Sti = [Sts]
		# true_minus_mean = data.values[i] - mean
		mean = np.mean(data.values[start:i + 1])
		print("mean: ", mean)
		means.append(mean)

	means_df = pd.Series(data=means, index=data.index)
	Sts = pd.Series(data=Sts, index=data.index)
	hits = pd.Series(data=hits["price"], index=hits["dates"])


	import matplotlib.pyplot as plt

	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	ax2 = ax1.twinx()

	data.plot(ax=ax1, color="red", label="Price")
	plt.ylabel("Close Price $")

	# means_df.plot(ax=ax2, color="blue", label="Average")
	# plt.ylabel("Daily Average")

	# Sts.plot(ax=ax2, color="blue", label="Sts")
	# plt.ylabel("Sts")

	# ax2.scatter(x=hits.index, y=hits.values, color="blue", label="Sti hits")
	# plt.ylabel("Price")

	ax1.scatter(x=hits.index, y=hits.values, color="blue", label="Sti hits")

	plt.xlabel("Date")
	plt.title("NVDA Stock Prices ")
	lines = ax1.get_lines() + ax2.get_lines()
	ax2.legend(lines, [l.get_label() for l in lines])
	plt.grid(True)
	plt.show()



	# print(x.head())
	# print(len(x))
	# print(type(y.stocks_data_dict))
	# print(type(y.get_stocks_data_dict))