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





