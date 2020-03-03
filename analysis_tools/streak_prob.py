from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
from configs_and_settings.settings import stock_data_settings
import pandas as pd

stock_symbols_list = stock_data_settings["stock_symbols"]
data_source = YahooStockDataFeed(stock_symbols_list)
data = data_source.stocks_market_data_dict["AAPL"]

c = data["Close"]
cdiff = c.diff()
cdiff_raw_copy = cdiff.copy()

cdiff_raw_copy[cdiff_raw_copy < 0] = 0 # drop in price
cdiff_raw_copy[cdiff_raw_copy > 0] = 1 # increase in price

drop_count = len(cdiff_raw_copy[cdiff_raw_copy == 0])
increase_count = len(cdiff_raw_copy[cdiff_raw_copy == 1])
print("Tot # of samples: {0}\nTot # of 0 labels: {1}\nTot # of 1 labels: {2}".format(len(cdiff_raw_copy), drop_count, increase_count))

vals = cdiff_raw_copy.values
bullish_streaks_list = []
bearish_streaks_list = []
# streaks_dict = {}
current_val = None
count = 0

for val in vals:
	if current_val is None and val == 1:
		count = 1
		current_val = 1
	elif current_val is not None and val == 1:
		count = count + 1
	elif current_val is not None and val != 1 and count != 0:
		bullish_streaks_list.append(count)
		count = 0
	else:
		continue

for val in vals:
	if current_val is None and val == 0:
		count = 1
		current_val = 0
	elif current_val is not None and val == 0:
		count = count + 1
	elif current_val is not None and val != 0 and count != 0:
		bearish_streaks_list.append(count)
		count = 0
	else:
		continue


def get_unique_elements(list):
	unique_elements = []
	for i in list:
		if i not in unique_elements:
			unique_elements.append(i)
		else:
			continue
	return unique_elements


bullish_unique_elements_list = get_unique_elements(bullish_streaks_list)
bearish_unique_elements_list = get_unique_elements(bearish_streaks_list)
unsigned_bearish_unique_elements_list = get_unique_elements(bearish_streaks_list)
bearish_unique_elements_list = [-x for x in bearish_unique_elements_list]

bullish_unique_elements_list.sort()
unsigned_bearish_unique_elements_list.sort()
bearish_unique_elements_list.sort(reverse=True)
# bearish_unique_elements_list.sort()


def get_streaks_count(streaks_list, unique_elements_list):
	streaks_dict = {}
	for unique_elements_count in unique_elements_list:
		streak = streaks_list.count(unique_elements_count)
		streaks_dict[unique_elements_count] = streak
	return streaks_dict


bullish_streaks_dict = get_streaks_count(bullish_streaks_list, bullish_unique_elements_list)
bearish_streaks_dict = get_streaks_count(bearish_streaks_list, unsigned_bearish_unique_elements_list)

# print("streaks_list produced: {0}".format(bullish_streaks_list))
# print("Unique elements in the list: {0}".format(bullish_unique_elements_list))
print("Bullish streak and durations: {0}".format(bullish_streaks_dict))
print("Bearish streak and durations: {0}".format(bearish_streaks_dict))

import matplotlib.pyplot as plt

down_count = list(bearish_streaks_dict.values())
bearish_counts = bearish_unique_elements_list
# bearish_counts = list(bearish_streaks_dict.keys())

up_count = list(bullish_streaks_dict.values())
bullish_counts = list(bullish_streaks_dict.keys())

print(down_count)
print(bearish_counts)
print(up_count)
print(bullish_counts)

combined_counts_vals = down_count + up_count
combined_counts_keys = bearish_counts + bullish_counts

plt.bar(combined_counts_keys, combined_counts_vals, color="green")
plt.xlabel("# of consecutive bullish days")
plt.ylabel("tot # of occurences")

plt.show()



