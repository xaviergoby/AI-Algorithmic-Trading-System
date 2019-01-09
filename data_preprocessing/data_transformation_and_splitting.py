# Author: Xavier O'Rourke Goby

import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def uni_and_multivar_ts_train_test_split(x, y, train_ratio):
    """
    :param x: a numpy array of your input data (features)
    :param y: a numpy array consisting of your output data (targets/labels/classes
    :param train_ratio: train_ratio: the ratio of training to testing data you want.
    i.e. train_ratio=0.7 means 70 you want 70% of your data set to be dedicated for training and the
    remaining 30% for testing!
    :return: a 4-tuple (x_train, y_train, x_test, y_test)
    """
    n_samples = max(x.shape)
    n_features = min(x.shape)

    if y.ndim == 1 or y.shape[0] != n_samples:
        y = y.reshape(n_samples, 1)
    if x.shape[0] != n_samples:
        x = x.reshape(n_samples, n_features)
    elif x.ndim == 1:
        x = x.reshape(n_samples, 1)

    train_samples_num = int(n_samples * train_ratio)

    x_train = x[:train_samples_num,:]
    y_train = y[:train_samples_num]
    x_test = x[train_samples_num:,:]
    y_test = y[train_samples_num:]

    return x_train, y_train, x_test, y_test

def normalize_x_y(x, y, min_max_range = (0, 1)):
    """
    :param x: a numpy array of your input data (features)
    :param y: a numpy array consisting of your output data (targets/labels/classes
    :param min_max_range: 2-tuple of the min and max values, (min, max), of the new normalized data. By default is (0, 1)
    :return: x, y, scaler_x, scaler_y
    """
    n_samples = max(x.shape)
    n_features = min(x.shape)

    if y.ndim == 1 or y.shape[0] != n_samples:
        y = y.reshape(n_samples, 1)
    if x.shape[0] != n_samples:
        x = x.reshape(n_samples, n_features)
    elif x.ndim == 1:
        x = x.reshape(n_samples, 1)

    scaler_x = MinMaxScaler(feature_range = min_max_range)
    scaler_y = MinMaxScaler(feature_range = min_max_range)
    x = scaler_x.fit_transform(x)
    y = scaler_y.fit_transform(y)
    return x, y, scaler_x, scaler_y

def unnormalize(trainPredict, testPredict, scaler_y, y_train, y_test):
    """
    This function is meant for reversing the normalization transformation which was
    applied to the data prior to being feed to the nn
    :param trainPredict: prediction made with x_train
    :param testPredict: prediction made with x_test
    :param scaler_y: the scaler_y obtained by normalization
    :param y_train:
    :param y_test:
    :return:
    """
    trainPredict = scaler_y.inverse_transform(trainPredict)  # y_train_pred
    y_train = scaler_y.inverse_transform(y_train)
    testPredict = scaler_y.inverse_transform(testPredict) # y_test_pred
    y_test = scaler_y.inverse_transform(y_test)
    return trainPredict, testPredict, y_train, y_test

def create_y_train_and_test_pred_array(y_train, y_test, trainPredict, testPredict):
    """
    :param y: a numpy array of the shifted true y/targets
    :param trainPredict:
    :param testPredict:
    :return:
    """
    np.set_printoptions(suppress=True)
    if y_train.ndim != 1 or y_test.ndim != 1 or trainPredict != 1 or testPredict != 1:
        y_train = y_train.reshape(len(y_train))
        y_test = y_test.reshape(len(y_test))
        trainPredict = trainPredict.reshape(len(trainPredict))
        testPredict = testPredict.reshape(len(testPredict))

    total_y_num = len(y_train) + len(y_test)
    train_pred_y_num = len(trainPredict)
    PredictPlot = np.ones((total_y_num))   # shape: (55,)
    PredictPlot[:train_pred_y_num] = trainPredict
    PredictPlot[train_pred_y_num:] = testPredict
    print("\ny_train shape:{0} & y y_test:{1}".format(y_train.shape, y_test.shape))
    print("\ntrainPredict shape:{0} & y testPredict:{1}".format(trainPredict.shape, testPredict.shape))
    print("post PredictPlot creation y_train [0]:{0}, y_train[-1]:{1}".format(y_train[0], y_train[-1]))
    print("post PredictPlot creation y_test [0]:{0}, y_test[-1]:{1}".format(y_test[0], y_test[-1]))
    print("post PredictPlot creation PredictPlot [0]:{0}, PredictPlot[-1]:{1}".format(PredictPlot[0], PredictPlot[-1]))
    print("\nPredictPlot shape:{0}".format(PredictPlot.shape))
    return PredictPlot

def uni_and_multivar_ts_matrix_train_test_split(x, y, train_ratio):
    """
    :param x: a numpy array or pd.DataFrame or pd.Series of your input data (features)
    :param y: a numpy array or pd.DataFrame or pd.Series of your output data (targets/labels/classes)
    :param train_ratio: train_ratio: the ratio of training to testing data you want.
    i.e. train_ratio=0.7 means 70 you want 70% of your data set to be dedicated for training and the
    remaining 30% for testing!
    :return: a 4-tuple (x_train, y_train, x_test, y_test)
    """
    n_samples = max(x.shape)
    n_features = min(x.shape)

    if isinstance(x, (pd.DataFrame, pd.Series)) and isinstance(y, (pd.DataFrame, pd.Series)):
        train_samples_num = int(n_samples * train_ratio)
        x_train = x[:train_samples_num]
        y_train = y[:train_samples_num]
        x_test = x[train_samples_num:]
        y_test = y[train_samples_num:]
        return x_train, y_train, x_test, y_test

    else:
        if y.ndim == 1 or y.shape[0] != n_samples:
            y = y.reshape(n_samples, 1)
        if x.shape[0] != n_samples:
            x = x.reshape(n_samples, n_features)
        elif x.ndim == 1:
            x = x.reshape(n_samples, 1)

        train_samples_num = int(n_samples * train_ratio)

        x_train = x[:train_samples_num,:]
        y_train = y[:train_samples_num]
        x_test = x[train_samples_num:,:]
        y_test = y[train_samples_num:]

        return x_train, y_train, x_test, y_test






