import numpy as np
import pandas as pd


class AdvancedBuyAndHoldStrategy:

    def __init__(self, data, ticker, signal, starting_balance=1000,
                 quantity=1, take_profit=0.1, max_open_orders_permitted=None,
                 max_capital_risk=0.1,
                 display_daily_performance=False, display_buy_event_info=False,
                 display_sell_event_info=False, display_hold_event_info=False):

        """
        This class implements a simple buy and hold strategy. This strategy STRICTLY ONLY allows for one open order to
        exist at a time (this means that before buying a 2nd stock in a company, the 1st one bought must be/have been sold a priori).

            Detailed Working Principle Explanation:
            -   You may specifiy the max number (quantity) of stocks of a company which can be bought for any given trade. Note that this
                fixes/sets the value of the number of stocks bought per trade toe the value passed to the "quantitiy" argument.
                I.e. the def value of 1 implies that strictly 1 stock in a comapny will be bought when ever the signal passed to the
                "signal" argument triggers an event to buy ( which is indicated by a 1 in the signal list).

        :param data: The pandas DataFrame of daily OHCLV and VWAP bars
        :param quantity: The maximum quantity of shares which can be bought. Is 1 by default.
        :param ticker: The companies index/ticker
        :param signal: A list of the signals encoded with one of the following 3 ints (1, 0, -1) w/ len = number of observations
        :param starting_balance: 1000$ by default
        """

        # numpy.ndarray w/ shape (len(data),) and ndim = 1
        # (can be loosely thought of as being a "row vector" ) since it will automatically broadcast up to an array of shape (1,len(data)) whenever necessary.
        self.close = data.Close.values.reshape(len(data))

        # numpy.ndarray w/ shape (len(data),) and ndim = 1
        self.dates = data.index.values.reshape(len(data))
        # numpy.ndarray w/ shape (len(data),) and ndim = 1
        self.signal = signal
        # self.signal = pd.Series(self.signal)

        self.take_profit = take_profit
        self.max_open_orders_permitted = max_open_orders_permitted
        self.max_capital_risk = max_capital_risk
        # pandas DataFrame consisting of: 1) a pandas.core.indexes.datetimes.DatetimeIndex index with pandas._libs.tslibs.timestamps.Timestamp type elements
        # 2) a pandas.core.series.Series type col named "Close" containing the true closing prices of numpy.float64 type
        # 3) a pandas.core.series.Series type col named "Signal" containig the (1,0,-1) type numpy.int32 encoded signal labels
        # self.dns =pd.DataFrame({"Close":self.close, "Signal":self.signal}, index=self.dates)
        self.n_days = len(data.index)
        self.q = quantity
        self.ticker = ticker
        self.initial_cash_balance = starting_balance
        self.cashBalance = starting_balance
        self.tradeHistory = []  # List of filled trades SHOULD PROBS REMOVE?
        self.open_orders = []
        self._display_daily_performance = display_daily_performance
        self._display_buy_event_info = display_buy_event_info
        self._display_sell_event_info = display_sell_event_info
        self._display_hold_event_info = display_hold_event_info
        self.long_positions_count = 0
        # self.n_trades = len(self.tradeHistory)

    def print_display_daily_performance(self, date_str, wk_day):
        if self._display_daily_performance is True:
            print('\n' * 2)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Start of day of trading~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Trading Date: {0}    Weekday: {1}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~".format(date_str, wk_day))


    def print_display_buy_event_info(self, buy_price, pre_trade_cash_balance,
                                     pre_trade_total_assets, pre_trade_open_orders,
                                     post_trade_cash_balance, post_trade_total_assets,
                                     post_trade_open_orders):

        if self._display_buy_event_info is True:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~BUY SIGNAL EVENT DETECTED - BUY ORDER TRIGGERED~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Pre-trade cash balance: ", pre_trade_cash_balance)
            print("Pre-trade total assets: ", pre_trade_total_assets)
            print("Pre-trade number of open orders: ", len(pre_trade_open_orders))
            print("BUY PRICE: ${0}".format(buy_price))
            print("Post-trade cash balance: ", post_trade_cash_balance)
            print("Post-trade total assets: ", post_trade_total_assets)
            print("Post-trade number of open orders: ", len(post_trade_open_orders))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End of trading day~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



    def print_display_sell_event_info(self, sell_price, pre_trade_cash_balance,
                                      pre_trade_total_assets, pre_trade_open_orders,
                                      post_trade_cash_balance, post_trade_total_assets,
                                      post_trade_open_orders):


        if self._display_sell_event_info is True:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SELL SIGNAL EVENT DETECTED - SELL ORDER TRIGGERED~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Pre-trade cash balance: ", pre_trade_cash_balance)
            print("Pre-trade total assets: ", pre_trade_total_assets)
            print("Pre-trade number of open orders: ", len(pre_trade_open_orders))
            print("SELL PRICE: ${0}".format(sell_price))
            print("Post-trade cash balance: ", post_trade_cash_balance)
            print("Post-trade total assets: ", post_trade_total_assets)
            print("Post-trade number of open orders: ", len(post_trade_open_orders))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End of trading day~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



    def print_display_hold_event_info(self, d):

        if self._display_hold_event_info is True:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~HOLD SIGNAL EVENT DETECTED - HOLD ORDER TRIGGERED~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Current cash balance: ", self.cashBalance)
            print("All open orders: ", self.open_orders)
            print("Number of open orders: ", len(self.open_orders))
            print("Total value of open orders: ", sum(self.open_orders))
            print("Current total assets: ", self.cashBalance + sum(self.open_orders))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End of trading day~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    def start_trading_sim(self):

        for d in range(len(self.signal)):

            # Assign to the var "date" the current date w/ a type <class 'numpy.datetime64'>
            date = self.dates[d]
            # Assign to the var "_date" the current date w/ a type <class 'pandas._libs.tslibs.timestamps.Timestamp'>
            _date = pd.to_datetime(str(date))
            # Assign to the var "date_str" the current date as a str type w/ a format %Y-%m-%d
            date_str = _date.strftime('%Y-%m-%d')
            # Assign to the var "wk_day" the current day of the working/business/trading week as a str type w/ a format %a
            wk_day = _date.strftime('%A')
            self.print_display_daily_performance(date_str, wk_day)
            position_size = self.q * self.close[d]


            if self.signal[d] == 1 and self.cashBalance*self.max_capital_risk <= position_size:

                pre_trade_open_orders = [x for x in self.open_orders]
                pre_trade_cash_balance = self.cashBalance
                pre_trade_total_assets = pre_trade_cash_balance + sum(pre_trade_open_orders)
                # percent_increase = [(new_value - og_value) / og_value] *
                self.open_orders.append(position_size)
                self.long_positions_count = self.long_positions_count + 1
                self.cashBalance = self.cashBalance - position_size

                post_trade_open_orders = [x for x in self.open_orders]
                post_trade_cash_balance = pre_trade_cash_balance - position_size
                post_trade_total_assets = post_trade_cash_balance + sum(post_trade_open_orders)

                self.print_display_buy_event_info(position_size, pre_trade_cash_balance,
                                                  pre_trade_total_assets, pre_trade_open_orders,
                                                  post_trade_cash_balance, post_trade_total_assets,
                                                  post_trade_open_orders)


            elif self.signal[d] == -1:
                # sell_date = date_str
                sell_price = self.close[d]
                sell_quantity_price = self.q * self.close[d]
                pct_change = lambda _buy_price: (sell_quantity_price - _buy_price) / _buy_price
                orders_to_sell = [x for x in self.open_orders if pct_change(x) > self.take_profit]
                orders_to_hold = [x for x in self.open_orders if pct_change(x) < self.take_profit]
                sell_orders_pct_change = [pct_change(x) for x in orders_to_sell]
                hold_orders_pct_change = [pct_change(x) for x in orders_to_hold]
                sell_orders_return = [sell_quantity_price - x for x in orders_to_sell]

                pre_trade_open_orders = [x for x in self.open_orders]
                pre_trade_cash_balance = self.cashBalance
                pre_trade_total_assets = pre_trade_cash_balance + sum(self.open_orders)

                self.open_orders = orders_to_hold
                self.cashBalance = self.cashBalance + sum(sell_orders_return) + sum(orders_to_sell)

                post_trade_open_orders = [x for x in self.open_orders]
                post_trade_cash_balance = pre_trade_cash_balance + sum(sell_orders_return) + sum(orders_to_sell)
                post_trade_total_assets = post_trade_cash_balance + sum(post_trade_open_orders)

                self.print_display_sell_event_info(sell_price, pre_trade_cash_balance,
                                                   pre_trade_total_assets, pre_trade_open_orders,
                                                   post_trade_cash_balance, post_trade_total_assets,
                                                   post_trade_open_orders)
                # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End of trading day~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            else:
                self.print_display_hold_event_info(d)
                # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End of trading day~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")




# if __name__ == "__main__":
#
#     tickers = ["AAPL", "AMZN", "ING", "INGA.AS"]
#     ticker = tickers[0]
#     apple = data_getter_funcs.get_stocks_data(ticker)
#     rsi_signal = RSI.RSI(apple, time_period=14,
#                          overbought_level=70,
#                          oversold_level=30)
#
#     rsi_signal_labels = rsi_signal.get_cat_sig_labels()
#     rsi_signal_encoded_labels = rsi_signal.get_cat_sig_int_encoded_labels()
#     print(type(rsi_signal))
#     print(type(rsi_signal_encoded_labels))
#
#     print("Number of observations:", len(rsi_signal_encoded_labels))
#     print("Number of Buy labels: ", rsi_signal_encoded_labels.count(1))
#     print("Number of Sell labels: ", rsi_signal_encoded_labels.count(-1))
#     print("Number of Hold labels: ", rsi_signal_encoded_labels.count(0))
#     # rsi_signal_encoded_labels = np.asarray(rsi_signal_encoded_labels)
#
#     starting_balance = 1000
#     quantity = 5
#     take_profit = 0.2
#     max_open_orders_permitted = 3
#     number_of_days = len(apple)
#     # number_of_days = len(apple) - 100
#
#     trader = AdvancedBuyAndHoldStrategy(apple, ticker,
#                                         rsi_signal_encoded_labels,
#                                         starting_balance=starting_balance, quantity=quantity,
#                                         take_profit=take_profit, max_open_orders_permitted=max_open_orders_permitted,
#                                         display_daily_performance=True, display_buy_event_info=True,
#                                         display_sell_event_info=True, display_hold_event_info=True)
#
#     trader.start_trading_sim()
#
#     print('\n' * 3)
#     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Portfolio Performance Feedback Information~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#
#     final_portfolio_value = trader.cashBalance + sum(trader.open_orders)
#
#     print("End of trading simulation portfolio value:   {0} $".format(round(final_portfolio_value, 2)))
#     print("End of trading simulation portfolio open orders value:   {0} $".format(round(sum(trader.open_orders), 2)))
#     print("End of trading simulation portfolio cash balance:   {0} $".format(round(trader.cashBalance, 2)))
#
#     pct_change = (final_portfolio_value - starting_balance) / starting_balance * 100
#
#     print("Percentage Total Change in Portfolio Value:   {0} %".format(round(pct_change, 2)))
#
#     print("\nStrategy optional parameters:\nCompany Yahoo stock index/indicator: {0}"
#           "\nStarting Balance: {1}\nMax quantity of shares to purchase: {2}"
#           "\nTake profit ratio: {3}\nMax number of open orders permitted: {4}"
#           "\nNumber of trading days simulated: {5}".format(ticker, starting_balance, quantity,
#                                                             take_profit, max_open_orders_permitted,
#                                                             number_of_days))
#
#     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")