from data_loader.download_stocks_basket_data import StockDataBasket
from data_preprocessing.lstm_data_preprocessing import LSTMDataAndPreprocessing
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from keras.optimizers import SGD
from keras.preprocessing.sequence import TimeseriesGenerator


stock_basket_idxs_dict = {"Semiconductors": ["INTC", "QCOM", "TXN", "ADI", "XLNX", "ASML", "NVDA", "AMD"]}
x = StockDataBasket(stock_basket_idxs_dict)
x.save_hdf5_stock_data_basket()
file_name = x.file_name
my_data_dict = x.load_specific_stock_basket_data(file_name)
stock_data_df = my_data_dict["ADI"]
n_prev = 50
lstm_data = LSTMDataAndPreprocessing(stock_data_df, 50, ["High", "Volume"], "Close")
complete_X_seq = stock_data_df[["High", "Volume"]].values
X_y_seq_lstm_data = lstm_data.get_X_y_seq_splits()
X = X_y_seq_lstm_data[0]
y = X_y_seq_lstm_data[1]
labels = lstm_data.generate_target_labels()
labels = lstm_data.generate_target_labels()
sides_dates_dict = labels[0]
sides_dict = labels[1]
# (timesteps,data_dim)
x_train, x_test, y_train, y_test = lstm_data.get_train_test_splits(0.7)

onehot_encoder = OneHotEncoder(sparse=False, categories="auto")
y_train = y_train.reshape(len(y_train), 1)
y_train_encoded = onehot_encoder.fit_transform(y_train)
# print(onehot_encoded)
onehot_encoder = OneHotEncoder(sparse=False, categories="auto")
y_test = y_test.reshape(len(y_test), 1)
y_test_encoded = onehot_encoder.fit_transform(y_test)

batch_size = 10
num_train_samples = len(x_train)
num_test_samples = len(x_test)
epochs = 1000
# num_of_batches_of_sampls =

# train_data_gen = TimeseriesGenerator(x_train, y_train_encoded,
#                                      length=look_back, sampling_rate=1,stride=1,
#                                batch_size=3)


# batch_input_shape needs the size of the batch: (numberofSequence,timesteps,data_dim)
# input_shape needs only the shape of a sample: (timesteps,data_dim)

data_dim = x_train.shape[2]
timesteps = x_train.shape[1]
# timesteps = 5
num_classes = y_train_encoded.shape[1]
# batch_input_shape = (5, timesteps, data_dim)
batch_input_shape = (2, 50, data_dim)
# input_shape = (timesteps, data_dim)
input_shape = (n_prev, data_dim)

def build_model(batch_input_shape, num_classes, input_shape):
	"""
	:param input_shape: (batch_size, timesteps, data_dim)
	:return:
	"""
	model = Sequential()
	model.add(LSTM(64, stateful=True, return_sequences=True, batch_input_shape=batch_input_shape))
	# model.add(LSTM(64, stateful=True, return_sequences=True, batch_input_shape=batch_input_shape))
	model.add(LSTM(32))
	model.add(Dense(num_classes, activation='softmax'))
	opt = SGD(lr=0.01)
	model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
	return model

model = build_model(batch_input_shape, num_classes, input_shape)
# model = build_model(batch_input_shape, num_classes, input_shape)

def data_gen(x, y):
	for dt in range(len(x)):
		# print("x[dt].shape: ", x[dt].shape, "y[dt].shape: ",y[dt].shape)
		# yield np.reshape(x[dt], (1,10,2)), y[dt]
		# yield np.reshape(x[dt], (1, 50, 2)), np.reshape(y[dt], (1, 3))
		yield np.reshape(x[dt], (1, n_prev, 2)), np.reshape(y[dt], (1, 3))

x_y_train_gen_func = data_gen(x_train, y_train_encoded)
x_y_test_gen_func = data_gen(x_test, y_test_encoded)
# x_train_gen_func = data_gen(x_train)
# y_train_encoded_gen_func = data_gen(y_train_encoded)
# Generate dummy training data
# x_train = np.random.random((1000, timesteps, data_dim))
# y_train = np.random.random((1000, num_classes))

# Generate dummy validation data
# x_val = np.random.random((100, timesteps, data_dim))
# y_val = np.random.random((100, num_classes))

# model.fit(x_train, y_train_encoded,batch_size=128, epochs=50, validation_data=(x_test, y_test_encoded))
history=model.fit_generator(x_y_train_gen_func,
							steps_per_epoch = num_train_samples // batch_size,
							epochs = epochs,
							validation_data = x_y_test_gen_func,
							# validation_data = x_y_test_gen_func)
							validation_steps = num_test_samples // batch_size)
# model.fit_generator(x_train_gen_func, )
# score = model.evaluate(x_test, y_test_encoded, batch_size=128)
# print(score)
# preds = model.predict(x_test)
# print(preds)