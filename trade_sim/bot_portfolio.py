# from backtesting.order import Order
from trade_sim.market_order import Order
import pandas as pd


class Portfolio:

    def __init__(self, cash_balance=1000, max_trade_risk_pct=50,
                 take_profit_pct=10, stop_loss_pct=10):
        self.current_date = None # type pandas._libs.tslibs.timestamps.Timestamp
        self.current_price = None # type numpy.float64
        self.current_portfolio_value = None
        self.cash_balance = cash_balance
        self.current_open_orders_tot_ret = 0
        # TM max pct of cash balance I am willing to invest on any single given trade
        self.max_trade_risk_pct = max_trade_risk_pct
        self.take_profit_pct = take_profit_pct
        self.stop_loss_pct = stop_loss_pct
        self.open_order = [] # change to "open_orders"
        self.current_open_orders_num = 0
        self.closed_order = [] # change to "closed_orders"
        self.daily_num_of_open_orders_history = []
        self.daily_cash_balance_history = []
        self.opened_orders_dates = []
        self.closed_orders_dates = []
        self.orders_history = []
        self.portfolio_history_dict = {"Date":[], "CashBalance[$]":[], "NetValue[$]":[], "OpenOrdersTotalReturn[$]":[], "#OfOpenOrders":[]}
        self.orders_record_book = {"OpenDate": [], "OrderPrice": [], "ClosedDate": [], "ClosedPrice": [], "OrderReturn[$]": [],
                                    "OrderReturnPct":[], "Shares#": [],"OrderOutcome": []}

    def portfolio_summary(self):
        msg = "\nCurrent portfolio value [$]:{0}\n" \
              "Cash balance [$]: {1}\n" \
              "Current open orders total returns: {2}\n" \
              "Current number of open orders: {3}".format(self.current_portfolio_value, self.cash_balance,
                                                          self.current_open_orders_tot_ret, self.current_open_orders_num)
        print(msg)

    def update_portfolio_current_date_and_price(self, current_date, current_price): # 1.1
        self.current_date = current_date
        self.current_price = current_price
        # if len(self.open_order != 0):
        #     print(self.open_order[0].current_return)

    def update_open_order(self): # 1.2
        print("Function called: {0}".format("self.update_open_order()"))
        # if len(self.open_order) != 0:
        for order_idx, order_obj in enumerate(self.open_order):
            order_obj.update_order(self.current_date, self.current_price) # 1.2.1
            print("order_obj.current_return: ", order_obj.current_return)
            if order_obj.closed is True:
                print("Barrier hit")
                closed_order = self.open_order.pop(order_idx)
                order_obj_i_num_shares = order_obj.num_shares
                tot_close_price = closed_order.closed_price * order_obj_i_num_shares
                # self.cash_balance = self.cash_balance + closed_order.current_value
                self.cash_balance = self.cash_balance + tot_close_price
                # self.cash_balance = self.cash_balance + closed_order.closed_price
                self.daily_cash_balance_history.append(self.cash_balance)
                self.orders_history.append(closed_order)
                self.closed_orders_dates.append(self.current_date)
                order_attributes = [closed_order.open_date, closed_order.open_price,
                                    closed_order.closed_date, round(closed_order.closed_price, 2),
                                    round(tot_close_price, 2), round(closed_order.return_pct, 2),
                                    closed_order.num_shares, closed_order.return_outcome]
                                    # round(closed_order.closed_return, 2), round(closed_order.return_pct,2), closed_order.return_outcome]
                for (key, value), attr in zip(self.orders_record_book.items(), order_attributes):
                    value.append(attr)
                print("break hit")
            # else:



            # self.update_open_orders_tot_value()
            #     break



    def update_open_orders_num(self): # 1.3
        new_open_orders_num = len(self.open_order)
        self.current_open_orders_num = new_open_orders_num
        print("Current number of open orders: {0}".format(self.current_open_orders_num))


    def update_open_orders_tot_value(self): # 1.4
        print("Function called: {0}".format("self.update_open_orders_tot_value()"))
        print("update_open_orders_tot_value returns self.open_order: ", self.open_order)
        print("type(update_open_orders_tot_value returns self.open_order): ", type(self.open_order))
        # if len(self.open_order) == 1:
        #     print("self.open_order[0].current_return: ", self.open_order[0].current_return)
        #     print("self.open_order[0].closed: ", self.open_order[0].closed)
        # print("type(self.open_order[0].current_return): ", type(self.open_order[0].current_return))
        if self.current_open_orders_num != 0:
            current_open_orders_tot_ret = 0
            for order_idx, order_obj in enumerate(self.open_order):
                order_obj.update_order(self.current_date, self.current_price) # 1.4.1
                print("order_obj.current_return type and return: ", type(order_obj.current_return), order_obj.current_return)
                print(type(order_obj.num_shares), order_obj.num_shares)
                order_obj_i_tot_return = order_obj.current_return
                # order_obj_i_tot_return = (order_obj.open_price + order_obj.current_return) * order_obj.num_shares
                current_open_orders_tot_ret = current_open_orders_tot_ret + order_obj_i_tot_return
            self.current_open_orders_tot_ret = current_open_orders_tot_ret
            return self.current_open_orders_tot_ret
        else:
            self.current_open_orders_tot_ret = 0
            return self.current_open_orders_tot_ret


    def update_portfolio(self,  current_date, current_price): # 1
        self.update_portfolio_current_date_and_price(current_date, current_price) # 1.1
        self.update_open_order() # 1.2
        self.update_open_orders_num() # 1.3
        # self.update_open_order()
        self.daily_cash_balance_history.append(self.cash_balance)
        self.daily_num_of_open_orders_history.append(self.current_open_orders_num)
        self.daily_num_of_open_orders_history.append(len(self.open_order))
        self.update_open_orders_tot_value() # 1.4
        open_orders_total_return = self.current_open_orders_tot_ret
        self.current_portfolio_value = self.cash_balance + open_orders_total_return
        # self.current_portfolio_value = self.cash_balance+self.open_order[0].return_pct if len(self.open_order) != 0 else self.cash_balance
        # open_orders_total_return = self.open_order[0].return_pct if len(self.open_order) != 0 else 0

        portfolio_info = [self.current_date, round(self.cash_balance, 2), round(self.current_portfolio_value, 2),
                          round(open_orders_total_return, 2), self.current_open_orders_num]
        for (key, value), info in zip(self.portfolio_history_dict.items(), portfolio_info):
            value.append(info)


    def get_current_max_tot_investment_amount(self):
        current_max_tot_investment_amount = self.cash_balance * (self.max_trade_risk_pct/100)
        return current_max_tot_investment_amount

    def get_long_pos_share_size(self):
        current_max_tot_investment_amount = self.get_current_max_tot_investment_amount()
        num_of_shares = current_max_tot_investment_amount//self.current_price
        print("get_long_pos_share_size() returns num_of_shares :", num_of_shares, " current_price: ", self.current_price)
        return num_of_shares

    def long_position_consultant(self):
        print("FOUND")
        if self.get_current_max_tot_investment_amount() > self.current_price:
            print("FOUND")
        # if self.update_current_max_tot_investment_amount() > self.current_price and len(self.open_order) == 0:
            max_shares_to_long = self.get_long_pos_share_size()
            print("max_shares_to_long: ", max_shares_to_long)
            order_buy_size = self.current_price * max_shares_to_long
            self.cash_balance = self.cash_balance - order_buy_size
            # self.cash_balance = self.cash_balance - self.current_price
            print(self.current_price)
            self.open_order.append(Order(self.current_date, self.current_price,
                                         self.take_profit_pct, self.stop_loss_pct,
                                         max_shares_to_long))
            self.opened_orders_dates.append(self.current_date)

    def create_and_get_portfolio_history_df(self):
        portfolio_history_df = pd.DataFrame(self.portfolio_history_dict, index=self.portfolio_history_dict["Date"])
        return portfolio_history_df

    def create_and_get_orders_record_book(self):
        orders_record_book = pd.DataFrame(self.orders_record_book, index=self.orders_record_book["OpenDate"])
        return orders_record_book

