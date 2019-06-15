import stock_data
from position_side_labeller import take_profit_stop_loss_labeller
import datetime as dt
# from pandas.datetools import BDay
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.3f' % x)


def weekly_labeller(stock_data):
    greater_than_avg_plus_1std = 0
    less_than_avg_plus_1std = 0
    stable = 0
    sides_dict = {"dates": [], "sides": []}
    stock_df = stock_data
    for index, row in stock_df.iterrows():
        if index.weekday() == 4:
            friday_idx = stock_df.index.get_loc(index)
            monday_idx = friday_idx - 4
            current_wk_except_friday = stock_df.iloc[monday_idx:friday_idx]
            for current_week_datetime_dt, current_week_day_row in current_wk_except_friday.iterrows():
                if current_week_datetime_dt.weekofyear != index.weekofyear:
                    current_wk_except_friday = current_wk_except_friday.drop(current_week_datetime_dt)
            avg = current_wk_except_friday.mean()["Close"]
            std = current_wk_except_friday.std()["Close"]
            print("The week w/o Friday df: {0}, corresponding mean(avg): {1} and corresponding std: {2}".format(current_wk_except_friday, avg, std))
            # if row["Close"] > avg + std:
            if row["Close"] > avg + std and len(current_wk_except_friday) == 4:
                sides_dict["dates"].append(index)
                sides_dict["sides"].append(1)
                greater_than_avg_plus_1std = greater_than_avg_plus_1std + 1
            # elif row["Close"] < avg - std:
            elif row["Close"] < avg - std and len(current_wk_except_friday) == 4:
                sides_dict["dates"].append(index)
                sides_dict["sides"].append(0)
                less_than_avg_plus_1std = less_than_avg_plus_1std + 1
            else:
                stable = stable + 1
    labelled_sides_df = pd.Series(sides_dict["sides"], index=sides_dict["dates"])
    return labelled_sides_df

wk_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

apple = stock_data.StockData("WDC")
# apple_df = apple.get_ema_smooth_stocks_data(trend_period=21)
apple_df = apple.get_stocks_data()
apple_close = apple_df.Close
apple_close_copy = apple_close.copy()
x = weekly_labeller(apple_df)
print(x)