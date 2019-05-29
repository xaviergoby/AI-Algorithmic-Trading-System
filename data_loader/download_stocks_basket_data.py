
# Semiconductor Equipment (and maybe "& Materials" or maybe "Memory"):
# Applied Materials, Inc. (AMAT)
# Analog Devices, Inc. (ADI)
# Xilinx, Inc. (XLNX)
# Brooks Automation, Inc. (BRKS)
# KLA-Tencor Corporation (KLAC)
# Lam Research Corporation (LRCX)
# Teradyne, Inc. (TER)
# Micron Technology, Inc. (MU)
# Taiwan Semiconductor Manufacturing (TSM)
# Broadcom Inc (AVGO)

# Stock indeces in use:
# stock_basket_idxs_dict = {"Semiconductors":["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}

from datetime import datetime
from data_loader.stock_data import StockData
import pandas as pd
import os


class StockDataBasket:

    def __init__(self, stock_idxs = {"Semiconductors": ["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}, end_date = datetime.today().strftime("%m-%d-%Y"), start_date = "01-06-2014"):
        """

        :param stock_idxs: The stocks Yahoo Finance index/ticker
        :param end_date:
        :param start_date:
        """
        self.industry_specific_stock_idxs = stock_idxs
        self.end_date = end_date
        self.start_date = start_date
        # self.industry_name = stock_idxs
        self.industry_name = list(self.industry_specific_stock_idxs.keys()) if len(list(self.industry_specific_stock_idxs.keys())) != 1     \
            else list(self.industry_specific_stock_idxs.keys())[0]
        self.industry_specific_stock_idxs_list = self.industry_specific_stock_idxs[self.industry_name]
        self.base_file_name = "{0}_stocks_data_{1}_{2}".format(self.industry_name, self.start_date,
                                                              self.end_date)
        self.file_name = os.path.join(os.path.abspath('../data'), self.base_file_name)

    def save_hdf5_stock_data_basket(self):
        stock_basket_store = pd.HDFStore(self.file_name)
        industry_idxs = self.industry_specific_stock_idxs_list
        for idx in industry_idxs:
            stock_data_obj = StockData(idx)
            stock_data = stock_data_obj.get_stocks_data()
            stock_data.to_hdf(stock_basket_store, key=idx)
        stock_basket_store.close()

    @staticmethod
    def load_hdf5_stock_data_basket(file_name):
        stock_basket_dict = {}
        stock_basket_store = pd.HDFStore(file_name)
        stock_basket_store_keys = stock_basket_store.keys()
        for idx_key in stock_basket_store_keys:
            stock_data = stock_basket_store.get(idx_key)
            stock_idx = idx_key.strip('/')
            stock_basket_dict[stock_idx] = stock_data
        stock_basket_store.close()
        return stock_basket_dict

    def save_and_load_hdf5_stock_data_basket(self):
        self.save_hdf5_stock_data_basket()
        file_name = self.file_name
        stock_basket_data = self.load_hdf5_stock_data_basket(file_name)
        return stock_basket_data

    # @staticmethod
    def load_specific_stock_basket_data(self, file_name):
        try:
            test_opening_file_var = open(file_name, 'r')
            stock_basket_dict = self.load_hdf5_stock_data_basket(file_name)
            return stock_basket_dict
        except FileNotFoundError:
            print("The file '{0}' was not found!")
            return None

    @staticmethod
    def load_hdf5_data_obj(hdf_file_obj):
        stock_basket_dict = {}
        # stock_basket_store = pd.HDFStore(file_name)
        stock_basket_store_keys = hdf_file_obj.keys()
        for idx_key in stock_basket_store_keys:
            stock_data = hdf_file_obj.get(idx_key)
            stock_idx = idx_key.strip('/')
            stock_basket_dict[stock_idx] = stock_data
        # stock_basket_store.close()
        return stock_basket_dict



if __name__ == "__main__":
    import os
    stock_basket_idxs_dict = {"Semiconductors": ["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}
    # x = StockDataBasket(stock_basket_idxs_dict)
    # x.save_hdf5_stock_data_basket()
    # file_name = x.file_name
    file_name = os.path.join(os.path.abspath('../data'), "Semiconductors_stocks_data_01-06-2014_05-16-2019")
    print(StockDataBasket(stock_basket_idxs_dict).load_specific_stock_basket_data(file_name))
    # my_data_dict = x.load_specific_stock_basket_data(file_name)
    # print(my_data_dict, len(my_data_dict), type(my_data_dict))

    # CAUSE FOR ERROR: MENTIONED ON THE INTERNET THAT THIS MIGHT BE BECAUSE OF NumPy's new version (I
    # just updated Numpy)!!!





