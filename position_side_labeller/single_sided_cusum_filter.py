from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
from configs_and_settings.settings import stock_data_settings

stock_symbols = stock_data_settings["stock_symbols"]
stock_data = YahooStockDataFeed(stock_symbols)
aapl_data = stock_data.stocks_data_dict["AAPL"]
aapl_close = aapl_data["Close"]

aapl_last_50_close = aapl_close.tail(50)

spos = 0
sneg = 0
restart_point = aapl_last_50_close.index[0]
pos_restart_point = aapl_last_50_close.index[0]
neg_restart_point = aapl_last_50_close.index[0]
for bar_date, bar_price in aapl_last_50_close[1:].iteritems():
    period_data = aapl_last_50_close.loc[restart_point:bar_date]
    est = period_data.mean()
    std = period_data.std()
    print(bar_date, bar_price)