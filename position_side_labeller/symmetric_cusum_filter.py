# The Symmetric CUMSUM filter


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def getTEvents(gRaw, h):
    tEvents_close = []
    tEvents, sPos, sNeg = [], 0, 0
    diff = np.log(gRaw).diff().dropna()
    # print(diff)
    for i in diff.index[1:]:
        try:
            pos, neg = float(sPos+diff.loc[i]), float(sNeg+diff.loc[i])
        except Exception as e:
            print(e)
            print(sPos+diff.loc[i], type(sPos+diff.loc[i]))
            print(sNeg+diff.loc[i], type(sNeg+diff.loc[i]))
            break
        sPos, sNeg=max(0., pos), min(0., neg)
        print("sPos:", sPos, "&", "sNeg:", sNeg, )
        if sNeg<-h:
            sNeg=0;tEvents.append(i)
            tEvents_close.append(gRaw[i])
        elif sPos>h:
            sPos=0;tEvents.append(i)
            tEvents_close.append(gRaw[i])
    return pd.DatetimeIndex(tEvents), tEvents_close


from data_loader.yahoo_stock_data_feed import YahooStockDataFeed
from configs_and_settings.settings import stock_data_settings

stock_symbols = stock_data_settings["stock_symbols"]
nvda_stock_data = YahooStockDataFeed(stock_symbols).stocks_data_dict["NVDA"]
nvda_close_data = nvda_stock_data["Close"]
h = 0.1 # Threshold (Filter size)
res = getTEvents(nvda_close_data, h)
myEvents = res[0]
tEvents_close = res[1]
logged = np.log(nvda_close_data).diff().dropna()
# print(myEvents)
print("len of apple.Close:", len(nvda_close_data))
print("len of myEvents:" ,len(myEvents))
print("len of tEvents_close:", len(tEvents_close))


# plt.plot(myEvents, tEvents_close, 'r')
plt.plot(nvda_close_data.index, nvda_close_data, 'b')
plt.show()
