from backtesting.portfolio import Portfolio

class TestStrategy:

    def __init__(self, close_ts, signal):
        self.close_ts = close_ts
        self.signal = signal
        self.current_date = None
        self.current_price = None
        self.portfolio_handler_cls = Portfolio()


    def start_trading(self):

        for d in range(len(self.close_ts)):

            # self.current_date = self.close_ts.index[d].strftime("%d-%m-%Y")
            self.current_date = self.close_ts.index[d]
            self.current_price = self.close_ts[d]
            self.portfolio_handler_cls.update_portfolio(self.current_date, self.current_price)


            if self.signal[d] == 1:
                # print("Signal: 1  on Date: {0}".format(self.current_date))
                self.portfolio_handler_cls.long_position_consultant()

            elif self.signal[d] == -1 or self.signal[d]:
                continue

if __name__ == "__main__":
    from data_loader.download_stocks_basket_data import StockDataBasket
    import os
    # stock_basket_idxs_dict = {"Semiconductors": ["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}
    # x = StockDataBasket(stock_basket_idxs_dict)
    # x.save_hdf5_stock_data_basket()
    # file_name = x.file_name
    file_name = os.path.join(os.path.abspath('../data'), "Semiconductors_stocks_data_01-06-2014_05-16-2019")
    my_data_dict = StockDataBasket().load_specific_stock_basket_data(file_name)
    # print(my_data_dict, len(my_data_dict), type(my_data_dict))






