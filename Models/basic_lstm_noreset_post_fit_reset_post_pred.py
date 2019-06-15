from data_loader.download_stocks_basket_data import StockDataBasket
from data_preprocessing.lstm_data_preprocessing import LSTMDataAndPreprocessing
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from keras.optimizers import SGD
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler


stock_basket_idxs_dict = {"Semiconductors": ["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}
x = StockDataBasket(stock_basket_idxs_dict)
# x.save_hdf5_stock_data_basket()
# file_name = x.file_name
# my_data_dict = x.load_specific_stock_basket_data(file_name)
pre_saved_data = x.load_specific_stock_basket_data("Semiconductors_stocks_data_01-06-2014_02-24-2019")
stock_data_df = pre_saved_data["ADI"]
n_prev = 50
lstm_data_handler_class = LSTMDataAndPreprocessing(stock_data_df, 50, ["High", "Volume"], "Close")
complete_X_seq = stock_data_df[["High", "Volume"]].values
X_y_seq_lstm_data = lstm_data_handler_class.get_X_y_seq_splits()
X = X_y_seq_lstm_data[0]
y = X_y_seq_lstm_data[1]
labels = lstm_data_handler_class.generate_target_labels()
sides_dates_dict = labels[0]
sides_dict = labels[1]
x_train, x_test, y_train, y_test = lstm_data_handler_class.get_train_test_splits(0.7)
# C:\Users\XGOBY\noname2\Models\Semiconductors_stocks_data_01-06-2014_02-24-2019
onehot_encoder = OneHotEncoder(sparse=False, categories="auto")
y_train = y_train.reshape(len(y_train), 1)
y_train_encoded = onehot_encoder.fit_transform(y_train)

onehot_encoder = OneHotEncoder(sparse=False, categories="auto")
y_test = y_test.reshape(len(y_test), 1)
y_test_encoded = onehot_encoder.fit_transform(y_test)

print("x_train :", x_train.shape, " & ", "y_train_encoded :",y_train_encoded.shape)
print("x_test :", x_test.shape, " & ", "y_test_encoded :", y_test_encoded.shape)



def scale(train, test, i):
	# fit scaler
	train = train[i]
	test = test[i]
	scaler = MinMaxScaler(feature_range=(-1, 1))
	scaler = scaler.fit(train)
	# transform train
	train = train.reshape(train.shape[0], train.shape[1])
	train_scaled = scaler.transform(train)
	# transform test
	test = test.reshape(test.shape[0], test.shape[1])
	test_scaled = scaler.transform(test)
	return scaler, train_scaled, test_scaled


	# print(scaler, train_scaled, test_scaled)
# scaler, x_train_scaled, x_test_scaled = scale(x_train, x_test)


# fit an LSTM network to training data
def fit_lstm(x_train, y_train, batch_size, nb_epoch, neurons):
	X = x_train
	y = y_train
	# X = X.reshape(X.shape[0], 1, X.shape[1])
	model = Sequential()
	model.add(LSTM(neurons, batch_input_shape=(batch_size, X.shape[1], X.shape[2]), stateful=False))
	# model.add(Dense(3, activation='softmax'))
	model.add(Dense(3))
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	for i in range(nb_epoch):
		model.fit(X, y, epochs=1, batch_size=batch_size, verbose=1, shuffle=False)
	return model

def forecast_lstm(model, batch_size, x_test, i):
	x_test = x_test[i].reshape(1, 50, 2)
	yhat = model.predict(x_test, batch_size=batch_size)
	# yhat = model.predict(x_test, batch_size=1)
	# yhat = model.predict(x_test)
	print("x_test: ", x_test)
	print("yhat: ", yhat)
	model.reset_states()
	return yhat


batch_size = 1
nb_epoch = 3
neurons = 32

# lstm_model = fit_lstm(x_train, y_train_encoded, batch_size, nb_epoch, neurons)
# predictions = list()
# # preds_num = len(y_test_encoded)
# preds_num = 10
# for i in range(preds_num):
# 	yhat = forecast_lstm(lstm_model, batch_size, x_test, i)
# 	predictions.append(yhat)



scale_nums = len(x_train) - 1
for i in range(scale_nums):
	scaler, train_scaled, test_scaled = scale(x_train, x_test, i)
	print("scaller :", scaler)
	print("train_scaled :", train_scaled)
	print("test_scaled :", test_scaled)
	print("i :", i)
	# print(scaler, train_scaled, test_scaled)
# scaler, x_train_scaled, x_test_scaled = scale(x_train, x_test)
