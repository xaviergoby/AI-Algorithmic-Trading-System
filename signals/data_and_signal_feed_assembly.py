import pandas as pd



class TradingSimDataAndSignalHandler:

    def __init__(self, raw_stock_data, predictions, prediction_dates):
        self.raw_stock_data = raw_stock_data
        self.prediction_dates = prediction_dates
        self.preds = predictions
        self.raw_stock_data_num = len(self.raw_stock_data)
        self.preds_num = len(self.preds)
        self.newest_pred_date = self.prediction_dates[-1]
        self.oldest_pred_date = self.prediction_dates[0]
        self.newest_pred_og_idx = self.raw_stock_data.index.get_loc(self.newest_pred_date)
        self.oldest_pred_og_idx = self.raw_stock_data.index.get_loc(self.oldest_pred_date)

    def compute_lacking_days_num(self):
        missing_days_num = self.raw_stock_data_num - self.newest_pred_og_idx
        return missing_days_num

    def create_truncated_trade_sim_stock_data(self):
        raw_stock_data_copy = self.raw_stock_data.copy()
        truncated_stock_data = raw_stock_data_copy[self.oldest_pred_og_idx:]
        return truncated_stock_data

    def create_complete_signal(self):
        missing_days_num = self.compute_lacking_days_num() - 1
        fillers = [0] * missing_days_num
        preds_list = self.preds.tolist()
        complete_signal = preds_list + fillers
        return complete_signal

    def create_ready_signal_stock_data_dict(self):
        data_and_signal_dict = {}
        dates = self.create_truncated_trade_sim_stock_data().index.tolist()
        signal = self.create_complete_signal()
        for date_num in range(len(dates)):
            data_and_signal_dict[dates[date_num]] = signal[date_num]
        return data_and_signal_dict


