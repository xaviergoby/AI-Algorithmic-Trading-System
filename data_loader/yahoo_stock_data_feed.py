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

    def __init__(self):
        self.stocks_data_dict = self.load_basket_of_stocks_data_dict()
        # self.basket_of_stocks_data_dict = self.get_basket_of_stocks_data()
        pass

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

    def load_basket_of_stocks_data(self, stock_symbol):
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
            stock_data_df = self.load_basket_of_stocks_data(stock_symbol)
            stocks_dict[stock_symbol] = stock_data_df
        return stocks_dict

    def save_data(self):
        pass


if __name__ == "__main__":
    y = YahooStockDataFeed()
    # txn = y.load_basket_of_stocks_data("txn")
    # t = y.get_stock_data(stock_symbol="TXN")
    nvda = y.stocks_data_dict["NVDA"]
    print(nvda.index)