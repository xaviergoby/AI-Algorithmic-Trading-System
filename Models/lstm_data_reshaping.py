# import pandas as pd
# import numpy as np
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import LSTM, Dropout
# from keras.utils import to_categorical
# from sklearn.model_selection import train_test_split


def verify_and_fix_data(X, y, time_steps = None,
                        batch_size = None, features = None,
                        num_of_class_labels = None):
	"""
	:param X: Observation/measurement data
	:param y: target class labels
	:param time_steps: total number of time steps/rows of X
	:param batch_size: number of time steps/rows of X per batch/sequence/time series
	:param features: tot num of features/num of cols of X
	:param num_of_class_labels: tot num of class labels for classification
	:return: X w/ shape (time_steps, batch_size, features &
	y w/ shape (time_steps, num_of_class_labels)
	"""
	
if __name__ == "__main__":
	from configs_and_settings.settings import stock_data_settings
	from data_loader.yahoo_stock_data_feed import YahooStockDataFeed


	# stock_symbols = stock_data_settings["stock_symbols"]
	# y = YahooStockDataFeed(stock_symbols)
	# stock_symbol = "NVDA"
	# x = y.stocks_data_dict[stock_symbol]
	import pandas as pd
	import numpy as np
	from position_side_labeller import take_profit_stop_loss_labeller
	from technical_indicators import rsi, sma_crossover
	from technical_indicators import sma
	from technical_indicators.new_daily_volitility import getDailyVol
	from signals.collect_and_merge_series_features import CollectAndMergeSeriesFeatures
	from technical_indicators import average_true_return
	from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
	from configs_and_settings.settings import stock_data_settings
	from data_preprocessing.data_transformation_and_splitting import uni_and_multivar_ts_matrix_train_test_split
	
	stock_data = YahooStockDataFeed(stock_data_settings["stock_symbols"])
	apple_df = stock_data.stocks_data_dict["AAPL"]
	# apple = stock_data.StockData("AAPL")
	# apple_df = apple.get_ema_smooth_stocks_data(trend_period=21)
	# apple_df = apple.get_stocks_data()
	apple_close = apple_df["Close"]
	apple_close_copy = apple_close.copy()
	
	expiration_days_limit = None
	take_profit_pct = 10
	stop_loss_pct = 10
	position_labels = take_profit_stop_loss_labeller.PositionSideLabeler(apple_close_copy,
	                                                                     take_profit_pct=take_profit_pct,
	                                                                     stop_loss_pct=stop_loss_pct,
	                                                                     expiration_days_limit=expiration_days_limit)
	position_labels.start_labeller()
	label_results_df = position_labels.get_results_df()
	sides = position_labels.get_side_labels_series()
	# sides = sides.shift(-1)
	sides = sides.dropna()
	days_elapsed_average = int(label_results_df["DaysElapsed"].describe()[1])
	days_elapsed_top_25_pct_q_avg = int(label_results_df["DaysElapsed"].describe()[4])
	days_elapsed_top_50_pct_q_avg = int(label_results_df["DaysElapsed"].describe()[5])
	days_elapsed_top_75_pct_q_avg = int(label_results_df["DaysElapsed"].describe()[6])
	days_elapsed_max = int(label_results_df["DaysElapsed"].describe()[7])
	
	technical_parameters = {"EMA": {"trend_period": days_elapsed_top_50_pct_q_avg},
	                        "SMA": {"trend_period_days": days_elapsed_top_50_pct_q_avg},
	                        "SMACrossOver": {"short_term_period": days_elapsed_top_25_pct_q_avg,
	                                         "long_term_period": days_elapsed_top_75_pct_q_avg, "threshold": 1},
	                        "RSI": {"time_period": 14, "overbought_level": 70, "oversold_level": 30},
	                        "getDailyVol": {"span0": days_elapsed_max}}
	
	# Initialising technical indicator class instances w/ specified argument parameters
	sma_signal = sma.SMA(apple_close, "AAPL", technical_parameters["SMA"]["trend_period_days"])
	ma_crossover_signal = sma_crossover.SMACrossOver(apple_close,
	                                                 technical_parameters["SMACrossOver"]["short_term_period"],
	                                                 technical_parameters["SMACrossOver"]["long_term_period"],
	                                                 technical_parameters["SMACrossOver"]["threshold"])
	rsi_signal = rsi.RSI(apple_close, technical_parameters["RSI"]["time_period"],
	                     technical_parameters["RSI"]["overbought_level"],
	                     technical_parameters["RSI"]["oversold_level"])
	daily_volatility = getDailyVol(apple_close, technical_parameters["getDailyVol"]["span0"]).dropna()
	atr14d = average_true_return.ATR(apple_df, period_length=days_elapsed_average).create_atr_series()
	# atr_vol = new_average_true_return.ATR(apple_df, period_length=14)
	
	# Computing the values of my technical indicators to use as features
	sma_signal_values = sma_signal.compute_and_get_sma_signal_values()
	sma_crossover_signal_values = ma_crossover_signal.get_sma_crossover_values()
	rsi_signal_values = rsi_signal.get_rsi_values()
	
	# Assembling all my technical indicator features together
	# collected_features = CollectAndMergeSeriesFeatures(sma21d=sma_signal_values, sma_crossover=sma_crossover_signal_values, rsi=rsi_signal_values, volatility=daily_volatility)
	collected_features = CollectAndMergeSeriesFeatures(rsi=rsi_signal_values,
	                                                   sma_crossover=sma_crossover_signal_values,
	                                                   volatility=daily_volatility,
	                                                   atr=atr14d)
	
	features_df = collected_features.get_features_df()
	features_df_copy = features_df.copy()
	n_features = len(features_df.columns)
	sides_copy = sides.copy()
	sides_copy = sides_copy.reindex(pd.DatetimeIndex(sides_copy.index))
	sides_copy = sides_copy[sides_copy.index.isin(features_df_copy.index)]
	features_df_copy = features_df_copy[features_df_copy.index.isin(sides_copy.index)]
	print("Length of features_df_copy:", len(features_df_copy), "Length of sides_copy: ", len(sides_copy))
	
	# Create pandas DataFrame of all data
	# res1 = pd.concat([labeller_result_df, features_df], axis=1).dropna()
	X_y_df = pd.concat([sides_copy, features_df_copy], axis=1).dropna()
	
	# Time-series to supervised learning problem necessary creation of forecasting observations via shifting
	# sides = sides.shift(-1)
	
	# Creating training and testing data sets by splitting up raw dataset consisting of X and y
	X = X_y_df[collected_features.features_names_list]
	y = X_y_df["LabelledSidesSeries"]
	x_train, y_train, x_test, y_test = uni_and_multivar_ts_matrix_train_test_split(X, y, 0.7)
	train_features, train_targets, test_features, test_targets = x_train, y_train, x_test, y_test
	features = X_y_df.columns[-n_features:]