from backtesting.order import Order
import pandas as pd


class Portfolio:

    def __init__(self, cash_balance=1000, max_trade_risk_pct=50,
                 take_profit_pct=10, stop_loss_pct=10):
        self.current_date = None
        self.current_price = None
        self.cash_balance = cash_balance
        # This represents the maximum percentage of my cash balance I am willing to invest on any single given trade
        self.max_trade_risk_pct = max_trade_risk_pct
        self.take_profit_pct = take_profit_pct
        self.stop_loss_pct = stop_loss_pct
        self.open_order = []
        self.closed_order = []
        self.daily_num_of_open_orders_history = []
        self.daily_cash_balance_history = []
        self.opened_orders_dates = []
        self.closed_orders_dates = []
        self.orders_history = []
        self.portfolio_history_dict = {"Date":[], "CashBalance[$]":[], "NetValue[$]":[], "OpenOrdersTotalReturn[$]":[], "#OfOpenOrders":[]}
        self.orders_record_book = {"OpenDate": [], "OrderPrice": [], "ClosedDate": [], "ClosedPrice": [], "OrderReturn": [],
                                    "OrderReturnPct":[], "OrderOutcome": []}

    def update_portfolio_current_date_and_price(self, current_date, current_price):
        self.current_date = current_date
        self.current_price = current_price

    def update_open_order(self):
        if len(self.open_order) != 0:
            for order_idx, order_obj in enumerate(self.open_order):
                order_obj.update_order(self.current_date, self.current_price)
                if order_obj.closed is True:
                    closed_order = self.open_order.pop(order_idx)
                    self.cash_balance = self.cash_balance + closed_order.closed_price
                    self.daily_cash_balance_history.append(self.cash_balance)
                    self.orders_history.append(closed_order)
                    self.closed_orders_dates.append(self.current_date)
                    order_attributes = [closed_order.open_date, closed_order.open_price, closed_order.closed_date, round(closed_order.closed_price, 2),
                                        round(closed_order.closed_return, 2), round(closed_order.return_pct,2), closed_order.return_outcome]
                    for (key, value), attr in zip(self.orders_record_book.items(), order_attributes):
                        value.append(attr)
                    break

    def update_portfolio(self,  current_date, current_price):
        self.update_portfolio_current_date_and_price(current_date, current_price)
        self.update_open_order()
        self.daily_cash_balance_history.append(self.cash_balance)
        self.daily_num_of_open_orders_history.append(len(self.open_order))

        portfolio_value = self.cash_balance+self.open_order[0].return_pct if len(self.open_order) != 0 else self.cash_balance
        open_orders_total_return = self.open_order[0].return_pct if len(self.open_order) != 0 else 0

        portfolio_info = [self.current_date, round(self.cash_balance, 2), round(portfolio_value, 2),
                          round(open_orders_total_return, 2), len(self.open_order)]
        for (key, value), info in zip(self.portfolio_history_dict.items(), portfolio_info):
            value.append(info)

    def long_position_consultant(self):
        if self.cash_balance * (self.max_trade_risk_pct/100) > self.current_price and len(self.open_order) == 0:
            self.cash_balance = self.cash_balance - self.current_price
            self.open_order.append(Order(self.current_date, self.current_price, self.take_profit_pct, self.stop_loss_pct))
            self.opened_orders_dates.append(self.current_date)

    def create_and_get_portfolio_history_df(self):
        portfolio_history_df = pd.DataFrame(self.portfolio_history_dict, index=self.portfolio_history_dict["Date"])
        return portfolio_history_df

    def create_and_get_orders_record_book(self):
        orders_record_book = pd.DataFrame(self.orders_record_book, index=self.orders_record_book["OpenDate"])
        return orders_record_book

