from scipy.fftpack import fft, ifft
from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
from configs_and_settings.settings import stock_data_settings
import matplotlib.pyplot as plt

stock_symbols = stock_data_settings["stock_symbols"]
data_src = YahooStockDataFeed(stock_symbols)
stock_data = data_src.stocks_data_dict["NVDA"]
close = stock_data["Close"]

fft_res = fft(close.values)
N = len(fft_res)

# plt.plot(fft_res, close.index)
plt.plot(close.index, fft_res)
plt.show()

