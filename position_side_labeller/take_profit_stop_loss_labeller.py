import pandas as pd
from data_loader import stock_data




class PositionSideLabeler:

    def __init__(self, close, take_profit_pct, stop_loss_pct, expiration_days_limit = None):
        """
        Labels of the 3 possible sides (barriers)  determined by the triggering one of the 3 potential events:
        - take_profit_pct_increase_limit : 1
        - stop_loss_pct_increase_limit : -1
        - expiration_days_limit : 0
        :param close: The closing prices of the companies stock
        :param take_profit_pct: int of  a positive percentage i.e. 10 for a 10% take-profit limit/threshold
        :param stop_loss_pct: int of  a positive percentage i.e. 10 for a -10% stop-loss limit/threshold
        :param expiration_days_limit: int representing the max number of days to hold before closing an "open order".
        More specifically this parameter is meant for adjusting the max extent of the horizon/future closing prices which will be
        considered for potential stop-loss and take-profit events being triggered. If neither of the previous two mentioned
        events is triggered before an "expiration_days_limit" number of days then a "hold" event is triggered!
        By default is None which if so means that the number of days till the expiration is equal to len(close)!
        """
        self.close = close
        self.take_profit_pct = take_profit_pct
        self.stop_loss_pct = stop_loss_pct
        self.expiration_days_limit = len(self.close) if expiration_days_limit is None else expiration_days_limit
        self.orders_opened_dates_list = []
        self.orders_opened_close_prices_list = []
        self.orders_closed_dates_list = []
        self.orders_closed_close_prices_list = []
        self.sides = []
        self.pct_changes_per_events_list = []
        self.days_elapsed_since_order_opened_list = []
        self.results_dict = {"BaseDate":[], "BasePrice":[], "HorizonLength":[], "DaysElapsed":[],
                             "BarrierDateHit":[], "Sides":[], "BarrierPriceHit":[], "PercentChange":[]}

    def start_labeller(self):
        outer_close_prices = self.close[: len(self.close) - 1]

        for current_date in range(len(outer_close_prices)):
            days_elapsed = 0
            future_data_slice = self.close[current_date + 1 : current_date + self.expiration_days_limit + 1]

            for future_date in range(len(future_data_slice)):
                days_elapsed = days_elapsed + 1
                pct_change = round( ( future_data_slice[future_date] - self.close[current_date] ) / self.close[current_date] * 100, 2 )

                if pct_change >= self.take_profit_pct:
                    result_dict_row_data = [self.close.index.date[current_date], self.close[current_date], len(future_data_slice), days_elapsed,
                                            future_data_slice.index.date[future_date], 1, future_data_slice[future_date], pct_change]
                    for (key, value), info in zip(self.results_dict.items(), result_dict_row_data):
                        value.append(info)
                    break

                elif pct_change <= -self.stop_loss_pct:
                    result_dict_row_data = [self.close.index.date[current_date], self.close[current_date],
                                            len(future_data_slice), days_elapsed,
                                            future_data_slice.index.date[future_date], -1,
                                            future_data_slice[future_date], pct_change]
                    for (key, value), info in zip(self.results_dict.items(), result_dict_row_data):
                        value.append(info)
                    break

                elif days_elapsed == self.expiration_days_limit:
                    result_dict_row_data = [self.close.index.date[current_date], self.close[current_date],
                                            len(future_data_slice), days_elapsed,
                                            future_data_slice.index.date[future_date], 0,
                                            future_data_slice[future_date], pct_change]
                    for (key, value), info in zip(self.results_dict.items(), result_dict_row_data):
                        value.append(info)
                    break

                else:
                    continue

    def get_results_df(self):
        res_df = pd.DataFrame(self.results_dict)
        return res_df

    def get_side_labels_series(self):
        dates = self.results_dict["BaseDate"]
        sides = self.results_dict["Sides"]
        side_labels_ts = pd.Series(data=sides, index=dates, name="LabelledSidesSeries")
        return side_labels_ts





