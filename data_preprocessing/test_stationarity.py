from statsmodels.tsa.stattools import adfuller
import pandas as pd
import matplotlib.pyplot as plt
import os

curr_dir = os.path.dirname(os.path.realpath(__file__))
file_path_def = os.path.join(curr_dir, "international-airline-passengers.csv")

def test_stationarity(ts, window):
    # Determing rolling statistics

    rolmean = ts.rolling.mean(window=window)
    rolstd = ts.rolling.std(window=window)


    # Plot rolling statistics:
    orig = plt.plot(ts, color='blue', label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(ts, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)


    # Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    # The null hypothesis is that the TS is non-stationary.
    # If the ‘Test Statistic’ is less than the ‘Critical Value’, we can reject the null hypothesis and say that the series is stationary.
    'Results of Dickey-Fuller Test:'
    dftest = adfuller(ts, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)

