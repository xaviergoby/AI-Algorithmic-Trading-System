import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# from data_loader.download_stocks_basket_data import StockDataBasket
import pandas as pd

# stock_basket_idxs_dict = {"Semiconductors": ["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}
# x = StockDataBasket(stock_basket_idxs_dict)
# x.save_hdf5_stock_data_basket()
# file_name = x.file_name
# my_data_dict = x.load_specific_stock_basket_data(file_name)
# print(my_data_dict, len(my_data_dict), type(my_data_dict))
# my_data_dict["ADI"].plot(y="Close")
# plt.show()


class StockDFDataBasketPlotter:

    def __init__(self):
        pass

    def plot_all_stocks(self, stocks_data_dict):
        """
        For plotting the closing prices of multiple stocks
        :param stocks_data_dict: a dict consisting of keys representing the ticker of each stock, e.g. "NVDA"
        and corresponding values which are pandas Dataframe type of the stocks OHCL data
        :return: a plot
        """
        stocks_tickers_list = list(stocks_data_dict.keys())
        ax = plt.gca() # Get the current Axes instance on the current figure matching the given keyword args, or create one.
        for stock_idx_i in stocks_tickers_list:
            stocks_data_dict[stock_idx_i].plot(y="Close", ax=ax, label=stock_idx_i)
            plt.title("Stocks Closing Prices")
        months = mdates.MonthLocator()
        ax.xaxis.set_minor_locator(months)
        plt.xlabel("Dates")
        plt.ylabel("Closing Price [$]")
        plt.grid(b=True, which="major")
        plt.show()

    def plot_all_stocks_daily_return(self, stocks_data_dict):
        stocks_tickers_list = list(stocks_data_dict.keys())
        ax = plt.gca() # Get the current Axes instance on the current figure matching the given keyword args, or create one.
        for stock_idx_i in stocks_tickers_list:
            stocks_data_dict[stock_idx_i].plot(y="Close", ax=ax, label=stock_idx_i)
            plt.title("Stocks Closing Prices")
        months = mdates.MonthLocator()
        ax.xaxis.set_minor_locator(months)
        plt.xlabel("Dates")
        plt.ylabel("Closing Price [$]")
        plt.grid(b=True, which="major")
        plt.show()


# StockDFDataBasketPlotter().plot_all_stocks_close_prices(my_data_dict)
# daily_cr = my_data_dict["ADI"]["Close"].cumprod()