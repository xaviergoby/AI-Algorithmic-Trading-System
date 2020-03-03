from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
from configs_and_settings.settings import stock_data_settings
from technical_indicators.ta_tools import TATools
from signals.collect_and_merge_series_features import CollectAndMergeSeriesFeatures



stock_symbol = "NVDA"
stock_symbols = stock_data_settings["stock_symbols"]

stocks_data_source = YahooStockDataFeed(stock_symbols)
stock_data = stocks_data_source.stocks_data_dict[stock_symbol]
print(stock_data)

rsi = TATools().rsi(stock_data, stock_symbol)
sma = TATools().sma(stock_data, stock_symbol)
macd = TATools().macd(stock_data, stock_symbol)



