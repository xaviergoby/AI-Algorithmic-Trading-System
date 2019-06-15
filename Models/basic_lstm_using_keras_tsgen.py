import numpy as np
import pandas as pd
from keras.preprocessing.sequence import TimeseriesGenerator
from time_series_preprocessing import TSProcessing
from data_loader.download_stocks_basket_data import StockDataBasket
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

stock_basket_idxs_dict = {"Semiconductors": ["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}
x = StockDataBasket(stock_basket_idxs_dict)
# C:\Users\XGOBY\noname2\Models\Semiconductors_stocks_data_01-06-2014_02-23-2019
file_name = r"C:\Users\XGOBY\noname2\Models\Semiconductors_stocks_data_01-06-2014_02-23-2019".replace('\\', '/')
stock_basket_df_data_dict = x.load_specific_stock_basket_data(file_name)
adi_stock_data = stock_basket_df_data_dict["ADI"]
adi_stock_close_array = adi_stock_data["Close"].values
train_array, test_and_val_array = TSProcessing().split_train_test_np_array(adi_stock_close_array, 0.7)
std = train_array.std()
print("post train and test val split shapes")
print(train_array.shape, test_and_val_array.shape)
train_array, test_and_val_array = TSProcessing().normalize_train_test_arrays_with_sklearn(train_array, test_and_val_array)
print("post norm shapes:")
print(train_array.shape, test_and_val_array.shape)
test_array, val_array = TSProcessing().split_train_test_np_array(test_and_val_array, 0.5)
print("post test val split shapes")
print(test_array.shape, val_array.shape)



n_input = 15
n_features = 1
batch_size = 1
epochs = 5
# train_set = adi_stock_close_array[:-6]
# test_set = adi_stock_close_array[-6:]
train_array = np.reshape(train_array, (len(train_array), n_features))
test_array = np.reshape(test_array, (len(test_array), n_features))
val_array = np.reshape(val_array, (len(val_array), n_features))
print(train_array.shape, val_array.shape, test_array.shape)
train_generator = TimeseriesGenerator(train_array, train_array, length=n_input, batch_size=batch_size)
test_generator = TimeseriesGenerator(test_array, test_array, length=n_input, batch_size=batch_size)
val_generator = TimeseriesGenerator(val_array, val_array, length=n_input, batch_size=batch_size)



# number of samples
print('Samples: {0}'.format(len(val_generator)))
# print each sample
for i in range(len(val_generator)):
	x, y = val_generator[i]
	print("x shape: {0}  &  y shape: {1}".format(x.shape, y.shape))
	print('{0} => {1}'.format(x, y))


model = Sequential()
model.add(LSTM(64, activation='relu', input_shape=(n_input, n_features), return_sequences=True))
model.add(LSTM(64, activation="relu", return_sequences=True))
model.add(LSTM(32, activation="relu", return_sequences=True))
model.add(LSTM(15, activation="relu"))
# model.add(Dropout(0.2))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

history = model.fit_generator(train_generator, epochs=epochs, verbose=2, validation_data=test_generator)
# score = model.evaluate_generator(val_generator)

# x_test = test_set[:-1]
# y_test = test_set[-1]
# x_test_reshaped = np.reshape(x_test, (1, n_input, n_features))
# yhat = model.predict(x_test_reshaped, verbose=0)
# print("prediction: {0}  &  true value: {1}".format(yhat, y_test))
# print(model.history.history["loss"])

import matplotlib.pyplot as plt

val_loss = history.history["val_loss"]
val_mean_absolute_error = history.history["val_mean_absolute_error"]
loss = history.history["loss"]
mean_absolute_error = history.history["mean_absolute_error"]
epochs_plot_series = range(1, len(loss) + 1)

fig = plt.figure()

# summarize history for accuracy
plt.subplot(2, 1, 1)
plt.plot(epochs_plot_series, mean_absolute_error, 'b', label='Validation loss')
plt.plot(epochs_plot_series, val_mean_absolute_error, 'r', label='Validation loss')
plt.title('model accuracy')
plt.ylabel('mae')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
# plt.show()
# summarize history for loss
plt.subplot(2, 1, 2)
plt.plot(epochs_plot_series, loss, 'b', label='Training loss')
plt.plot(epochs_plot_series, val_loss, 'r', label='Validation loss')
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


# print("Metrics names: {0}".format(model.metrics_names))
# print("Scores: {0}".format(score))
# print("score[1] * std: {0}".format(score[1] * std))





for i in range(len(val_generator)):
	x, y = val_generator[i]
	print("x shape: {0}  &  y shape: {1}".format(x.shape, y.shape))
	print("x len: {0}  &  y len: {1}".format(len(x), len(y)))
	pred = model.predict_on_batch(x)
	print("~~~~~~~~~~~~~PREDICTION: {0}".format(pred))
	print('{0} => {1}'.format(x, y))







