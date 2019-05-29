import pandas as pd
import numpy as np
# import os
# from data_loader.download_stocks_basket_data import StockDataBasket
import abc

class StockPerformanceToolkit:

    @staticmethod
    def compute_daily_returns(stock_closing_prices_pd_series):
        daily_returns = stock_closing_prices_pd_series.diff(1)
        return daily_returns

    @staticmethod
    def compute_daily_pct_returns(stock_closing_prices_pd_series):
        daily_returns = stock_closing_prices_pd_series.pct_change(1)
        return daily_returns

    @staticmethod
    def compute_stock_basket_daily_returns(dict_of_pd_series_stock_closing_prices):
        stocks_basket_returns_dict = {}
        for stock_idx in list(dict_of_pd_series_stock_closing_prices.keys()):
            stocks_basket_returns_dict[stock_idx] = StockPerformanceToolkit().compute_daily_returns(dict_of_pd_series_stock_closing_prices[stock_idx])
        return stocks_basket_returns_dict