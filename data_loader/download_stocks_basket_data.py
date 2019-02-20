
# Semiconductor Equipment (and maybe "& Materials" or maybe "Memory"):
# Applied Materials, Inc. (AMAT)
# Analog Devices, Inc. (ADI)
# Xilinx, Inc. (XLNX)
# Brooks Automation, Inc. (BRKS)
# KLA-Tencor Corporation (KLAC)
# Lam Research Corporation (LRCX)
# Teradyne, Inc. (TER)
# Micron Technology, Inc. (MU)

# Stock indeces in use:
# stock_basket_idxs_dict = {"Semiconductors":["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}

from datetime import datetime
from data_loader.stock_data import StockData
import pandas as pd


class StockDataBasket:

    def __init__(self, stock_idxs, end_date = datetime.today().strftime("%m-%d-%Y"), start_date = "01-06-2014"):
        self.industry_specific_stock_idxs = stock_idxs
        self.end_date = end_date
        self.start_date = start_date
        self.industry_name = list(self.industry_specific_stock_idxs.keys()) if len(list(self.industry_specific_stock_idxs.keys())) != 1     \
            else list(self.industry_specific_stock_idxs.keys())[0]
        self.industry_specific_stock_idxs_list = self.industry_specific_stock_idxs[self.industry_name]
        self.file_name = "{0}_stocks_data_{1}_{2}".format(self.industry_name, self.start_date, self.end_date)

    def save_stock_data_basket_as_h5_file(self):
        stock_basket_store = pd.HDFStore(self.file_name)
        industry_idxs = self.industry_specific_stock_idxs_list
        for idx in industry_idxs:
            stock_data_obj = StockData(idx)
            stock_data = stock_data_obj.get_stocks_data()
            stock_data.to_hdf(stock_basket_store, key=idx)
        stock_basket_store.close()

    def load_h5_file_stock_data_basket(self):
        stock_basket_dict = {}
        stock_basket_store = pd.HDFStore(self.file_name)
        stock_basket_store_keys = stock_basket_store.keys()
        for idx_key in stock_basket_store_keys:
            stock_data = stock_basket_store.get(idx_key)
            stock_idx = idx_key.strip('/')
            stock_basket_dict[stock_idx] = stock_data
        stock_basket_store.close()
        return stock_basket_dict


# if __name__ == "__main__":
#     stock_basket_idxs_dict = {"Semiconductors": ["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}
#     x = StockDataBasket(stock_basket_idxs_dict)
#     x.save_stock_data_basket_as_h5_file()
#     my_data_dict = x.load_h5_file_stock_data_basket()




