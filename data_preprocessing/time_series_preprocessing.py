import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler




class TSProcessing:


    @staticmethod
    def split_train_test_df(df_data, ratio):
        timesteps_num = len(df_data)
        train_timesteps_num = int(timesteps_num * ratio)
        train = df_data.iloc[:train_timesteps_num,]
        test = df_data.iloc[train_timesteps_num:,]
        return train, test

    @staticmethod
    def split_train_test_np_array(np_array, ratio):
        timesteps_num = max(np_array.shape)
        train_timesteps_num = int(timesteps_num * ratio)
        train = np_array[:train_timesteps_num,]
        test = np_array[train_timesteps_num:,]
        return train, test

    @staticmethod
    def get_all_zero_divisors(n):
        all_zero_divisors = []
        n = int(n)
        for i in range(1, n + 1):
            if (n % i == 0):
                all_zero_divisors.append(i)
        return all_zero_divisors

    @staticmethod
    def normalize_train_test_arrays_with_sklearn(train, test):
        train_samples_num = max(train.shape)
        test_samples_num = max(test.shape)
        features_num = min(train.shape)
        if train.ndim == 1:
            train = np.reshape(train, (train_samples_num, 1))
        else:
            train = np.reshape(train, (train_samples_num, features_num))
        if test.ndim == 1:
            test = np.reshape(test, (test_samples_num, 1))
        else:
            test = np.reshape(test, (train_samples_num, features_num))
        scaler = MinMaxScaler(feature_range=(0, 1))
        fitted_scaler = scaler.fit(train)
        train_scaled = fitted_scaler.transform(train)
        test_scaled = fitted_scaler.transform(test)
        return train_scaled, test_scaled

    @staticmethod
    def normalize_train_test_arrays(train_array, test_array):
        mean = train_array.mean(axis=0)
        train_array -= mean
        std = train_array.std(axis=0)
        train_array /= std
        test_array -= mean
        test_array /= std
        return train_array, test_array

    @staticmethod
    def standardize_train_test_arrays_with_sklearn(train, test):
        train_samples_num = max(train.shape)
        test_samples_num = max(test.shape)
        features_num = min(train.shape)
        train = np.reshape(train, (train_samples_num, features_num))
        test = np.reshape(test, (test_samples_num, features_num))
        scaler = StandardScaler()
        fitted_scaler = scaler.fit(train)
        train_scaled = fitted_scaler.transform(train)
        test_scaled = fitted_scaler.transform(test)
        return train_scaled, test_scaled



if __name__ == "__main__":
    from load_data.download_stocks_basket_data import StockDataBasket
    stock_basket_idxs_dict = {"Semiconductors": ["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}
    x = StockDataBasket(stock_basket_idxs_dict)
    # C:\Users\XGOBY\noname2\Models\Semiconductors_stocks_data_01-06-2014_02-23-2019
    file_name = r"C:\Users\XGOBY\noname2\Models\Semiconductors_stocks_data_01-06-2014_02-23-2019".replace('\\','/')
    stock_basket_df_data_dict = x.load_specific_stock_basket_data(file_name)
    adi_stock_data = stock_basket_df_data_dict["ADI"]
    train_df, test_df = TSProcessing().split_train_test_df(adi_stock_data, 0.7)
    train_array, test_array = TSProcessing().split_train_test_np_array(adi_stock_data.iloc[:,1:].values, 0.7)
    train_array_standardised, test_array_standardised = TSProcessing().standardize_train_test_arrays_with_sklearn(train_array, test_array)
    train_array_normalized, test_array_normalized = TSProcessing().normalize_train_test_arrays_with_sklearn(train_array, test_array)