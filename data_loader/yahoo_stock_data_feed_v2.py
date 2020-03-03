import pandas_datareader as web
import pandas as pd
from data_loader.abstract_stock_data_feeder_class import AbstractStockDataFeed
from configs_and_settings.settings import default_settings
from datetime import datetime
import os
import json
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class YahooStockDataFeed(AbstractStockDataFeed):
	name = "YahooStockDataFeed"
	source = "yahoo"

	def __init__(self, stock_symbols_list=None):
		self.stock_symbols_list = stock_symbols_list
	# self.stock_symbols_list = stock_symbols_list if isinstance(stock_symbols_list, list) else [stock_symbols_list]

	def update_json_stock_data_metadata(self, data_dict):
		metadata_abspath = os.path.join(os.path.abspath(self.data_dir_path), "stock_data_metadata.json")
		if os.path.exists(metadata_abspath):
			print("The json file: {0} exists!".format(metadata_abspath))
			with open(metadata_abspath) as json_data:
				res = json.load(json_data)
				print(res.keys())
		else:
			print("Creating {0} file...".format(metadata_abspath))
			with open(metadata_abspath, 'w') as f:
				json.dump(data_dict, f)
				print("updates metadata with: {0}".format(data_dict))
			# print(res)
			# return res
		
	def get_stored_stock_data_file_names(self):
		file_names = os.listdir(os.path.abspath(self.data_dir_path))
		file_names_with_ext = [filename for filename in file_names if filename.endswith(".csv")]
		return file_names_with_ext

	def get_stored_data_stock_symbols(self):
		file_names = os.listdir(os.path.abspath(self.data_dir_path))
		file_names_with_ext = [filename for filename in file_names if filename.endswith(".csv")]
		present_stock_csv_files = [stock_symbol.split('.')[0] for stock_symbol in file_names_with_ext]
		return present_stock_csv_files
	# pass
	# return self.get_stored_data_stock_symbols()

	def compare_present_and_missing_stock_data(self):
		present_stock_data_symbols = self.get_stored_data_stock_symbols()
		missing_stock_symbols = []
		for stock_symbol in self.stock_symbols_list:
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

	def get_stock_data(self, stock_symbol, start_date=None, end_date=None):
		if start_date and end_date is None:
			stock_data = web.DataReader(stock_symbol, data_source=self.source, start=self.start_date, end=self.end_date)
		# stock_data = web.DataReader(stock_symbol, data_source=self.source, start=self.start_date, end=self.end_date)
			return stock_data

	def save_stock_data(self, stock_symbol, stock_data_df):
		stock_data_csv_name = "{0}.csv".format(stock_symbol)
		stock_data_csv_full_path = os.path.join(os.path.abspath(self.data_dir_path), stock_data_csv_name)
		stock_data_df.to_csv(stock_data_csv_full_path) # //TODO

	def download_basket_of_stocks_data(self):
		for stock_symbol in self.stock_symbols_list:
			stock_data = self.get_stock_data(stock_symbol)
			self.save_stock_data(stock_symbol, stock_data)

	def load_basket_of_stocks_df(self, stock_symbol):
		stock_data_csv_name = "{0}.csv".format(stock_symbol)
		stock_data_csv_full_path = os.path.join(os.path.abspath(self.data_dir_path), stock_data_csv_name)
		stock_data_df = pd.read_csv(stock_data_csv_full_path, index_col=0, parse_dates=True) # //TODO
		return stock_data_df


	def load_basket_of_stocks_data_dict(self):
		if self.compare_present_and_missing_stock_data() is not None:
			self.download_basket_of_stocks_data()
			print("hey")
		stocks_dict = {}
		for stock_symbol in self.stock_symbols_list:
			stock_data_df = self.load_basket_of_stocks_df(stock_symbol)
			stocks_dict[stock_symbol] = stock_data_df
		return stocks_dict

	@property
	def stocks_market_data_dict(self):
		stock_market_data_dict = self.load_basket_of_stocks_data_dict()
		return stock_market_data_dict


if __name__ == "__main__":
	from configs_and_settings.settings import stock_data_settings
	# stock_symbols = stock_data_settings["stock_symbols"]
	data_src = YahooStockDataFeed()
	# stock_symbol_list = ["AAPL", "AMD"]
	# stock_symbol = "FB"
	data_src.stock_symbols_list = ["AMD", "AAPL"]
	# data_src.stock_symbols_list = ["FB", "AAPL"]
	data = data_src.stocks_market_data_dict["AAPL"]
	print(data.head(1))
	print(data.tail(1))
	# data_src.update_json_stock_data_metadata({"AAPL":{"start_date":"10/10/2019"}})
