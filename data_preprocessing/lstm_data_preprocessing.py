import numpy as np
import pandas as pd

class LSTMDataAndPreprocessing:

    def __init__(self, data_set_df, pre_train_data_points, feature_cols_names, true_target_or_label_col_name):
        """

        :param data: a single pandas dataframe
        :param prev_points: int of the number of previous data points/samples meant for training/learning
        in order to predict the next single data point
        """
        self.data_set_df = data_set_df
        self.pre_train_data_points = pre_train_data_points
        self.data_set_df_len = len(self.data_set_df)
        self.feature_cols_names = feature_cols_names
        self.true_target_or_label_col_name = true_target_or_label_col_name
        self.labelled_sides_dates_dict = None

    def get_X_y_seq_splits(self):
        labelled_sides_and_dates = self.generate_target_labels()[1]
        labelled_sides_list = labelled_sides_and_dates["sides"]
        labelled_sides_corresponding_dates_list = labelled_sides_and_dates["dates"]
        X = []
        y = labelled_sides_list
        for row in range(self.data_set_df_len - self.pre_train_data_points):
            X.append(self.data_set_df[self.feature_cols_names].iloc[row:row + self.pre_train_data_points].values)
        X_array = np.array(X)
        y_array = np.array(labelled_sides_list)
        return X_array, y_array

    def generate_target_labels(self):
        greater_than_avg_plus_1std = 0
        less_than_avg_plus_1std = 0
        stable = 0
        sides = []
        labelled_sides_dates_dict = {}
        labelled_sides_dict = {"dates":[], "sides":[] }
        for row_id in range(self.data_set_df_len - self.pre_train_data_points):
            seq_avg_close_price = self.data_set_df["Close"].iloc[row_id:row_id + self.pre_train_data_points].mean()
            seq_std_close_price = self.data_set_df["Close"].iloc[row_id:row_id + self.pre_train_data_points].std()
            true_close_price = self.data_set_df["Close"].iloc[row_id + self.pre_train_data_points]
            if true_close_price > seq_avg_close_price + seq_std_close_price:
                labelled_sides_dict["dates"].append(self.data_set_df.index[row_id])
                labelled_sides_dict["sides"].append(1)
                labelled_sides_dates_dict[self.data_set_df.index[row_id]] = 1
                greater_than_avg_plus_1std = greater_than_avg_plus_1std + 1
            elif true_close_price < seq_avg_close_price - seq_std_close_price:
                labelled_sides_dict["dates"].append(self.data_set_df.index[row_id])
                labelled_sides_dict["sides"].append(-1)
                labelled_sides_dates_dict[self.data_set_df.index[row_id]] = -1
                less_than_avg_plus_1std = less_than_avg_plus_1std + 1
            else:
                labelled_sides_dict["dates"].append(self.data_set_df.index[row_id])
                labelled_sides_dict["sides"].append(0)
                labelled_sides_dates_dict[self.data_set_df.index[row_id]] = 0
                stable = stable + 1
        self.labelled_sides_dates_dict = labelled_sides_dates_dict
        return labelled_sides_dates_dict, labelled_sides_dict

    def get_train_test_splits(self, ratio):
        X_y_arrays = self.get_X_y_seq_splits()
        X = X_y_arrays[0]
        y = X_y_arrays[1]
        available_data_points_num = self.data_set_df_len - self.pre_train_data_points
        train_data_points_num = int(available_data_points_num * ratio)
        X_train = X[:train_data_points_num]
        X_test = X[train_data_points_num:]
        y_train = np.reshape(y[:train_data_points_num], (len(y[:train_data_points_num]), 1))
        y_test = np.reshape(y[train_data_points_num:], (len(y[train_data_points_num:]), 1))
        return X_train, X_test, y_train, y_test

    def normalize_seq_windows(self):
        pass

#
if __name__ == "__main__":
    from data_loader.download_stocks_basket_data import StockDataBasket
    stock_basket_idxs_dict = {"Semiconductors": ["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}
    x = StockDataBasket(stock_basket_idxs_dict)
    x.save_hdf5_stock_data_basket()
    file_name = x.file_name
    my_data_dict = x.load_specific_stock_basket_data(file_name)
    stock_data_df = my_data_dict["ADI"]
    lstm_data = LSTMDataAndPreprocessing(stock_data_df, 50, ["High", "Volume"], "Close")
    X_y_seq_lstm_data = lstm_data.get_X_y_seq_splits()
    X = X_y_seq_lstm_data[0]
    y = X_y_seq_lstm_data[1]
    labels = lstm_data.generate_target_labels()
    sides_dates_dict = labels[0]
    sides_dict = labels[1]
    #(timesteps,data_dim)
    x_train, x_test, y_train, y_test = lstm_data.get_train_test_splits(0.7)