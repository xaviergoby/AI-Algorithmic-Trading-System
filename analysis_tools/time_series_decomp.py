from statsmodels.tsa.seasonal import seasonal_decompose
from dateutil.parser import parse
from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
from configs_and_settings.settings import stock_data_settings
import matplotlib.pyplot as plt
import pandas as pd

stock_symbols = stock_data_settings["stock_symbols"]
data_src = YahooStockDataFeed(stock_symbols)
# ['INTC', 'NVDA', 'MU', 'QCOM', 'AMD', 'XLNX', 'ASML', 'TXN', 'AAPL']
stock_symbol = 'ASML'
stock = data_src.stocks_data_dict[stock_symbol]
close1 = stock["Close"]
# close2 = close1.resample('D')
close2 = close1.resample('D').ffill()
# close2 = close.asfreq("D", method="pad")
# close3 = close2.fillna(method='ffill')
print(len(close1), len(close2))
# close.asfreq("D", method="pad")


def get_all_stocks_ts_resids(stocks_data_dict, model="multiplicative"):
	stocks_ts_resids_dict = {}
	stock_idxs = list(stocks_data_dict.keys())
	for stock_idx in stock_idxs:
		stock_market_close_data = stocks_data_dict[stock_idx]["Close"]
		stock_daily_close_data = stock_market_close_data.resample('D').ffill()
		stock_components = seasonal_decompose(stock_daily_close_data, model=model, freq=30)
		stock_resid = stock_components.resid
		stocks_ts_resids_dict[stock_idx] = stock_resid
	pd_dt_index = stock_daily_close_data.index
	stocks_resids_df = pd.DataFrame(data=stocks_ts_resids_dict, index=pd_dt_index)
	return stocks_resids_df


stocks_data_dict = data_src.stocks_market_data_dict
resids = get_all_stocks_ts_resids(stocks_data_dict)
resids.plot(y="AAPL")
plt.title("residuals components")
corrs = resids.corr()
# corrs.plot(kind="barh")
plt.show()
# print(resids.keys())








# freq = 252
# freq = close2.index.freqstr
# Both the trend and residuals components are of np.nan type within the
# slice [0:126] (so indexes 0,1,....124,125 and not incl. idx 126)
# So this means that the first 126 elements of both the residuals and trend
# np.arrays are np.nan! This is b/c 252 / 2 = 126

# model = "multiplicative"
# model = "additive"

# res = seasonal_decompose(close2, model=model, freq=freq)
# res = seasonal_decompose(close2, model=model, extrapolate_trend="freq")
# trend = res.trend
# seasonal = res.seasonal
# resid = res.resid
#
#
# plot_name = "{1} {0} freq= {2}".format(model, stock_symbol, freq)
# res.plot().suptitle(plot_name)
# plt.grid(True)
# plt.show()
