import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.style.use('dark_background')
import pandas as pd


class StockDataPlotter:

	def __init__(self):
		pass

	def plot_close(self, data, *args, **kwargs):
		"""

		:param data:
		:param kwargs: close_prices, dates, symbol, name,
		:return:
		"""
		fig, ax = plt.subplots()


		if isinstance(data, pd.DataFrame):
			close_pd_series = data["Close"]
			myplot = close_pd_series.plot(ax = ax, color="r")
		elif isinstance(data, pd.Series):
			myplot = close_pd_series.plot(ax=ax, color="r")

		ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
		plt.gcf().autofmt_xdate()

		if "symbol" in list(kwargs.keys()):
			ax.legend([kwargs["symbol"]], loc = "upper right")
		if "name" in list(kwargs.keys()):
			plt.title("Daily Close Prices of {0} Stocks".format(kwargs["name"]))


		plt.xlabel("Dates")
		plt.ylabel("Close prices [$]")
		plt.grid(which="both")
		plt.xticks(rotation=45)
		plt.show()

if __name__ == "__main__":
	from configs_and_settings.settings import stock_data_settings
	from data_loader.yahoo_stock_data_feed import YahooStockDataFeed

	stock_symbols = stock_data_settings["stock_symbols"]
	stock_symbol = "NVDA"

	src = YahooStockDataFeed(stock_symbols)
	data = src.stocks_data_dict[stock_symbol]
	StockDataPlotter().plot_close(data, symbol = stock_symbol, name = "Nvidia")