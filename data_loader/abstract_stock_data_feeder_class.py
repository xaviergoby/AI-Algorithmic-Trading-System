from abc import ABC, abstractmethod
from configs_and_settings import stock_tickers
from configs_and_settings.settings import default_settings
from configs_and_settings.settings import stock_data_settings
from datetime import datetime, timedelta
import os

class AbstractStockDataFeed(ABC):
    name = "AbstractTradeBot"
    num_of_days = 2920 # 365 * 8
    end_date = datetime.today().strftime("%m-%d-%Y")  # most recent date w/ format mm/dd/yy
    start_date_obj = datetime.today() - timedelta(days=num_of_days)
    start_date = start_date_obj.strftime("%m-%d-%Y")
    data_dir_path = os.path.abspath('../data')
    stock_symbols = stock_data_settings["stock_symbols"]


    @abstractmethod
    def get_stored_data_stock_symbols(self):
        """
        This function is meant to look for OHCLV & VWAP data of a stock which are already present/stored
        in the data folder and is then meant to return the names of those .csv data files - the stock symbols
        :return: list of str stock symbols
        """
        pass

    @abstractmethod
    def compare_present_and_missing_stock_data(self):
        """
        This method is meant to compare the list of stock symbols in the json settings
        with those being used as file names for their data. It then returns a list of stocks symbols
        which are present in the json settings but not in the data dir.
        :return:
        """
        pass

    @property
    @abstractmethod
    def get_date_today(self):
        pass

    @abstractmethod
    def get_stock_data(self):
        pass

    @abstractmethod
    def save_stock_data(self):
        pass

    @abstractmethod
    def download_basket_of_stocks_data(self):
        pass

    @abstractmethod
    def load_basket_of_stocks_data(self):
        pass

    @abstractmethod
    def load_basket_of_stocks_data_dict(self):
        pass

    @abstractmethod
    def save_data(self):
        pass











