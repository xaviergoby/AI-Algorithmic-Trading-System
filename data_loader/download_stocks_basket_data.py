
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
from stock_data import StockData
import pandas as pd


class StockDataBasket:

    def __init__(self, stock_idxs, end_date = datetime.today().strftime("%m-%d-%Y"), start_date = "01-06-2014"):
        self.stock_idxs = stock_idxs
        self.end_date = end_date
        self.start_date = start_date
        self.industries = list(self.stock_idxs.keys()) if len(list(self.stock_idxs.keys())) != 1     \
            else list(self.stock_idxs.keys())[0]
        self.indexes = list(self.stock_idxs.values())

    def save_stock_data_to_hdf5(self, stock_data_df, hdf5_file_name, idx):
        with pd.HDFStore(hdf5_file_name) as store:
            store.put(idx, stock_data_df)

    def save_data_as_h5_file_(self, industry_name, hdf5_file_name):
        industry_idxs = self.stock_idxs[industry_name]
        for idx in industry_idxs:
            stock_data_obj = StockData(idx)
            stock_data = stock_data_obj.get_stocks_data()
            self.save_stock_data_to_hdf5(stock_data, hdf5_file_name, idx)


# if __name__ == "__main__":
#     stock_basket_idxs_dict = {"Semiconductors": ["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}
#     x = StockDataBasket(stock_basket_idxs_dict)
#     file_name = "{0}_stocks_data_{1}_{2}".format(x.industries, x.start_date, x.end_date)
#     x.save_data_as_h5_file_("Semiconductors", hdf5_file_name = file_name)
#     data = pd.HDFStore(file_name)
#     print(data.get(data.keys()[0]))
#     data.close()





