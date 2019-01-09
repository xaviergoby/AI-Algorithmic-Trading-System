
class Order:

    def __init__(self, open_date, open_price, take_profit_pct, stop_loss_pct):
        self.open_date = open_date    # D_i
        self.open_price = open_price       # P_i
        self.take_profit_pct = take_profit_pct                                              # %TP
        self.stop_loss_pct = stop_loss_pct if stop_loss_pct > 0 else abs(stop_loss_pct)     # %SL
        self.take_profit_price = (1 + self.take_profit_pct / 100) * self.open_price         # P_tp
        self.stop_loss_price = (1 - self.stop_loss_pct / 100) * self.open_price             # P_sl
        self.return_pct = None
        self.current_return = None
        self.closed = False
        self.closed_date = None            # D_f
        self.closed_price = None           # P_f
        self.closed_return = None
        self.return_outcome = None
        # self.attrs_dict = {"OpenDate": [], "OrderPrice": [], "ClosedDate":[], "ClosedPrice":[], "OrderReturn": [], "OrderOutcome": []}

    def update_order(self, current_date, current_price):

        self.return_pct = ((current_price - self.open_price) / self.open_price) * 100
        self.current_return = current_price - self.open_price

        if current_price >= self.take_profit_price or current_price <= self.stop_loss_price:
            self.closed_date = current_date
            self.closed_price = current_price
            self.closed_return = current_price - self.open_price
            self.closed = True
            if current_price >= self.take_profit_price:
                self.return_outcome = 1
            elif current_price <= self.stop_loss_price:
                self.return_outcome = 0

        # if self.filled is True:
        # print("\n" ,"~"*20 ,"Closing (Filling) of Order Initiated", "~"*20)
        #     print("Filling Order Opened On: {0} @ a Price of: {1}$".format(self.open_date, round(self.open_price, 2)))
        #     print("Reason: {0}".format("Take-Profit Limit Hit" if self.ret > 0 else "Stop-Loss Limit Hit"))
        #     print("Filled Date: {0}  &  Filled Price: {1}$".format(self.filled_date, round(self.filled_price, 2)))
        #     print("Fractional Return: {0}  &  Percentage Return: {1}  &  Dollar Value: {2}$".format(round(self.ret, 4), round(self.return_pct, 2), round(self.value, 2)))






#
# if __name__ == "__main__":
#     import datetime
#     import numpy as np
#     # from datetime import datetime
#     today = datetime.datetime.today().date()
#     date_list = [today - datetime.timedelta(days=x) for x in range(0, 10)]
#     date_list.reverse()
#     price = 95.50
#     take_profit_pct = 10
#     stop_loss_pct = 10
#     order = Order(today, price, take_profit_pct, stop_loss_pct)
#     prices = np.linspace(96, 110, 10)
#     for price, date in zip(prices, date_list):
#         if order.closed is not True:
#             order.update_order(date, price)
#             print(price, date)
#         elif order.closed is True:
#             # attrs_dict = {"OpenDate": [], "OrderPrice": [], "ClosedDate":[], "ClosedPrice":[], "OrderReturn": [], "OrderOutcome": []}
#             attrs = [order.open_date, order.open_price, order.closed_date, round(order.closed_price, 2), round(order.closed_return, 2), order.return_outcome]
#             for (key, value), attr in zip(order.attrs_dict.items(), attrs):
#                 print(key, value, attr)
#                 value.append(attr)
#             break
#
#
#     # print(combined)