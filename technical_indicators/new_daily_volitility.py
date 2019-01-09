import pandas as pd
from data_loader import stock_data

# =======================================================
# Daily Volatility Estimator (from 31 AinFML)
## for wtvr reason dates are not aligned for return calculation
## must account for it for computation


def getDailyVol(close, span0=100):
    """
    Function for computing the daily volatility and subsequently reindexing
    the result to match the input "close"
    :param close:
    :param span0:
    :return:
    """
    df0 = close.index.searchsorted(close.index - pd.Timedelta(days=1))
    df0 = df0[df0 > 0]
    # df0 = pd.Series(close.index[df0–1], index=close.index[close.shape[0] - df0.shape[0]:])
    df0=(pd.Series(close.index[df0-1],index=close.index[close.shape[0]-df0.shape[0]:]))
    df0 = close.loc[df0.index] / close.loc[df0.values].values - 1  # daily returns
    df0 = df0.ewm(span=span0).std()
    # return df0.dropna()
    return df0
#
# apple = data_getter_funcs.get_stocks_data("AAPL")
# close_copy = apple.Close.copy()
# print("apple close_copy len: ", len(close_copy))
# dvol = getDailyVol(close_copy)
# print(close_copy.head())
# print(dvol.head())
# print("\ndvol len: ", len(dvol))
# print("dvol type: ", type(dvol))
# # print("index first 5 elements: ", dvol.index[0:5])
# # print("index last 5 elements: ", dvol.index[-5:])
# print("dvol head: ", dvol.head())
# print("dvol tail: ", dvol.tail())
# no_nan_dvol = dvol.dropna()
# print("\nno_nan_dvol len: ", len(no_nan_dvol))
# print("no_nan_dvol head: ", no_nan_dvol.head())
# print("no_nan_dvol tail: ", no_nan_dvol.tail())