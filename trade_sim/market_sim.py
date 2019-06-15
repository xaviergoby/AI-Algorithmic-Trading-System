from trade_sim.classical_trade_bot import ClassicalTradeBot
from trade_sim.predictive_trade_bot import PredictiveTradeBot
from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
from technical_indicators.technical_indicator_funcs import SMA
from technical_indicators.ta_tools import TATools
import pandas as pd
from technical_indicators.technical_indicator_funcs import RSI_Xavier
from technical_indicators.technical_indicator_funcs import RSI_Timo


data_feed = YahooStockDataFeed()


# signal = [0, 0, 0, 1, -1, 0, 0, 0, 1, 0, 0, -1, 0, 1, 0, 0]

# norm_bot = ClassicalTradeBot(signal)
# pred_bot = PredictiveTradeBot(signal)

# norm_bot.trade()
# pred_bot.trade()
# print(norm_bot.performance(), pred_bot.performance())

# ClassicalTradeBot: H, H, H, B, S, H, H, H, B, H, H, S, H, B, H, H   w/   final current_cash_sum = 1100
# PredictiveTradeBot: H, H, H, B, S, H, H, H, B, H, H, S, H, H, H, H   w/   final current_cash_sum = 1200

nvda = data_feed.stocks_data_dict["NVDA"]
# nvda_sma = TATools().sma(nvda, "NVDA")
# nvda_ema = TATools().ema(nvda, "NVDA")
nvda_rsi = TATools().rsi(nvda, "NVDA")
# nvda_rsi1 = RSI_Xavier(nvda)
nvda_rsi2 = RSI_Timo(nvda)
# print(nvda.head())
# print(nvda_rsi1.tail())
print(nvda_rsi2.tail())
print(nvda_rsi2.name)
# print(nvda_rsi1.name)
# print(nvda_rsi2.name)
print(nvda_rsi.tail())
print(nvda_rsi.name)

# nvda2 = pd.DataFrame(nvda["Close"], index=range(len(nvda)))
# print(nvda2.tail())
# numeric_indeces = [x for x in range(len(nvda))]