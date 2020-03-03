import pandas as pd
raw_data = pd.read_csv(r"C:\Users\XGOBY\noname2\data\AD Historical Data.csv")
print(raw_data)

og_dates = raw_data["Date"]
# %b : Sep  %   %m : 09
# $d : 30
# %Y : 2020
og_dates_strf = "%b %d, %Y"
# new date format: YY-mm-dd
new_dates_str = "%Y-%m-%d"
raw_data['Date'] = pd.to_datetime(raw_data['Date'])

raw_subdata = raw_data[["Date", "Price"]]
dates = raw_subdata["Date"].tolist()
price = raw_subdata["Price"].iloc[::-1].values
dates.reverse()
new_subdata = pd.DataFrame(data=price, index=dates)

import matplotlib.pyplot as plt

new_subdata.resample('BQS').ffill().plot(title="Ahold Business QonQ Stock Price[€]", grid=True, legend=False)
plt.xlabel("Dates[YY-mm-dd]")
plt.ylabel("Price[€]")
plt.grid(b=True, which='major', axis="both", color='k', linestyle='-')
plt.grid(b=True, which='minor', axis="both", color='grey', linestyle='-', alpha=0.2)
# ax = plt.gca()
plt.show()
