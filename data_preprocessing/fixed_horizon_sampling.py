import numpy as np


class SlidingWindowSampling:
	
	def __init__(self, data, time_steps, features):
		"""
		This class is meant for creating multiple samples of data from a single time-series sequence which
		is then later feed to an LSTM model.
		The arg for the data parameter should be a pandas DataFrame containing a "Close" column and 1 or more
		other columns. Note that the arg for the features parameter can only the names of columns which are
		already present in data!
		The number of samples created by a time-series consisting of a tot of n # of observations is equal
		to n - time_steps. Each of these samples which then consist of a time_steps # of observations!
		
		So, in short (w/ notation and terminology):
		observations = input variables think x
		targets = output variables think y
		n = tot # of observations in time-series data = len(data)
		dts = time_steps = "step size" = the number of observations per sample
		K = samples = the tot num of samples possible = n - dts
		Each sample can be thought of as being denoted by X_k where k = 0, 1, 2, ... K
		E.g. given data = [0, 1, 2, 3, 4, 5, 6, 7, 8]  &  time_steps = 3
		sample k -> [x_0, x_1, x_2, ... x_dts, y_k]  =  [X_k, y_k]
		where X_k = [x_0, x_1, x_2, .... x_dts]
		
		so sample 0 -> [x_0, x_1, x_2, y_0]  =  [X_0, y_0] = [0, 1, 2, 3]
		where X_0 [0, 1, 2] and y_0 = [3]
		
		Tk = pd.DatetimeIndex interval slice of length dts + 1 of sample k where k = 0, 1, 2, ..., K
		Where the first dts # of elements (each of pd0.Timestamp type) correspond w/ x_0, x_1, x_2, .... x_dts
		and the last element (also of pd.Timestap type) corresponds w/ y_k
		so e.g. T_0 = [x_0.date, x_1.date, x_2.date, y_0.date] = [X_0.date, y_0.date]
		T_0 [Monday, Tuesday, Wednesday, Thursday] where X_0.date = [Monday, Tuesday, Wednesday] & y_0.date = [Thursday]
		
		:param data: pandas DataFrame with "Close" col and 1 or more feature cols
		:param time_steps: int for the (fixed horizon) step size
		:param features: list containing str type name of the cols in the data pd.DataFrame to use as input vars
		"""
		self.data = data
		self.time_steps = time_steps
		self.features = features
		self.close = self.data["Close"] # aka target/output variables/data
		self.features_df = self.data[self.features]  # aka observation/input variables/data
		self.samples = len(self.data) - self.time_steps
		self.K = self.samples
		self.dts = self.time_steps
		self.Fs = len(self.features) # number of features
		
	def print_process_info(self, k, Tk, Tk_start, Tk_end, Tk_plus_1_start, Xk, yk):
		print("\n", "~"*10, "Iteration {0}".format(k), "~"*10)
		print("T^{0} Start date: {1}".format(k, Tk_start.date()))
		print("T^{0} End date: {1}".format(k, Tk_end.date()))
		print("T^{0} DatetimeIndex Slice: {1}".format(k, Tk))
		print("T^{0} Start date: {1}   (the date of corresponding target)".format(k + 1, Tk_plus_1_start.date()))
		print("X{0}: {1}".format(k, Xk))
		print("y{0}: {1}".format(k, self.data.loc[Tk_plus_1_start]))
		
	def label_target_via_prev_day_obs_price(self, yk, Tk_end):
		if yk > self.close.loc[Tk_end]: # if the price on day i is greater than the price on day i-1
			yk_label = np.array([1, 0])
		elif yk < self.close.loc[Tk_end]:# if the price on day i is less than the price on day i-1
			yk_label = np.array([0, 1])
		elif yk == self.close.loc[Tk_end]:
			yk_label = np.array([0, 1])
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LABEL [0,0]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LABEL [0,0]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LABEL [0,0]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LABEL [0,0]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LABEL [0,0]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LABEL [0,0]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LABEL [0,0]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LABEL [0,0]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LABEL [0,0]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LABEL [0,0]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LABEL [0,0]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LABEL [0,0]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		return yk_label
	
	def get_fixed_horizon_obs_and_target_samples(self, print_process_info=False):
		Xk_array_list = []
		yk_array_list = []
		yk_label_array_list = []
		for k in range(self.K):
			Tk = self.close.index[k:k+self.dts+1]
			Tk_observations = Tk[:-1] # pandas DatetimeIndex
			Tk_target = Tk[-1] # pandas Timestap
			Tk_start = Tk_observations[0]
			Tk_end = Tk_observations[-1]
			Xk = self.features_df.loc[Tk_observations]
			yk = self.close.loc[Tk_target]
			yk_label = self.label_target_via_prev_day_obs_price(yk, Tk_end)
			Xk_array_list.append(Xk.values)
			yk_array_list.append(yk)
			yk_label_array_list.append(yk_label)
			if print_process_info is True:
				self.print_process_info(k, Tk, Tk_start, Tk_end, Tk_target, Xk, yk)
			else:
				continue
		X = np.asarray(Xk_array_list)
		y = np.asarray(yk_array_list)
		y_labels = np.asarray(yk_label_array_list)
		return X, y, y_labels
		# return X, y
	

		

if __name__ == "__main__":
	from configs_and_settings.settings import stock_data_settings
	from data_loader.yahoo_stock_data_feed import YahooStockDataFeed


	stock_symbols = stock_data_settings["stock_symbols"]
	data_src = YahooStockDataFeed(stock_symbols)
	stock_symbol = "AAPL"
	stock_data = data_src.stocks_data_dict[stock_symbol]
	stock_close = stock_data["Close"]
	time_steps = 14
	samples = stock_data.shape[0] - time_steps
	from tests.test_load_data import features_df
	import pandas as pd
	res = pd.concat([stock_close, features_df], axis=1).dropna()
	# res = pd.concat([features_df, stock_close], axis=1)
	features = list(features_df.columns)
	# labeller = SlidingWindowSampling(stock_data.tail(100), time_steps=time_steps, features=["Close", "High"])
	labeller = SlidingWindowSampling(res, time_steps=time_steps, features=features)
	X, y, y_labels = labeller.get_fixed_horizon_obs_and_target_samples(print_process_info=True)
	print(X.shape, y.shape, y_labels.shape)
	
	import sklearn.model_selection as model_selection

	x_train, x_test, y_train, y_test = model_selection.train_test_split(X, y_labels, train_size=0.75, test_size=0.25)

	from keras.models import Sequential
	from keras.layers import LSTM, Dense

	timesteps = X.shape[1]
	num_classes = y_labels.shape[1]
	features = X.shape[2]

	# expected input data shape: (batch_size, timesteps, data_dim)
	model = Sequential()
	model.add(LSTM(64, return_sequences=True,
	               input_shape=(timesteps, features)))  # returns a sequence of vectors of dimension 32
	model.add(LSTM(64, return_sequences=True))  # returns a sequence of vectors of dimension 32
	model.add(LSTM(32, return_sequences=True))  # returns a sequence of vectors of dimension 32
	model.add(LSTM(32, return_sequences=True))  # returns a sequence of vectors of dimension 32
	model.add(LSTM(32))  # return a single vector of dimension 32
	model.add(Dense(2, activation='sigmoid'))

	model.compile(loss='binary_crossentropy',
	              optimizer='adam',
	              metrics=['accuracy'])

	history = model.fit(x_train, y_train,
	          batch_size=64, epochs=200,
	          validation_data=(x_test, y_test))

	import matplotlib.pyplot as plt

	# Plot training & validation accuracy values
	plt.plot(history.history['acc'])
	plt.plot(history.history['val_acc'])
	plt.title('Model accuracy')
	plt.ylabel('Accuracy')
	plt.xlabel('Epoch')
	plt.legend(['Train', 'Test'], loc='upper left')
	plt.show()

	# Plot training & validation loss values
	plt.plot(history.history['loss'])
	plt.plot(history.history['val_loss'])
	plt.title('Model loss')
	plt.ylabel('Loss')
	plt.xlabel('Epoch')
	plt.legend(['Train', 'Test'], loc='upper left')
	plt.show()


