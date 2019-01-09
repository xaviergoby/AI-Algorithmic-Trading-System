from technical_indicators.technical_indicators import *
from data_loader.data_sources import *

data = get_stocks_data()
data_with_rsi = MACD_signal_line(data)
print(data_with_rsi)
