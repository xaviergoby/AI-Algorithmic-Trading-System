from analysis_tools.performance_tools import StockPerformanceToolkit
from data_loader.data_loading_tools import get_hdf_data
from utils.plot_compare_multiple_ts import StockDFDataBasketPlotter
from signals.collect_and_merge_series_features import CollectAndMergeSeriesFeatures

file_rel_path = "data/Semiconductors_stocks_data_01-06-2014_05-21-2019"
data_dict = get_hdf_data("data/Semiconductors_stocks_data_01-06-2014_05-21-2019")
# data = get_hdf_data("data/Semiconductors_stocks_data_01-06-2014_05-21-2019")["NVDA"]["Close"]
# print("type(data): ", type(data))
# nvda_daily_returns = StockPerformanceToolkit().compute_daily_returns(get_hdf_data("data/Semiconductors_stocks_data_01-06-2014_05-21-2019")["NVDA"]["Close"])
# nvda_daily_returns = StockPerformanceToolkit().compute_daily_returns(data)
# nvda_daily_pct_returns = StockPerformanceToolkit().compute_daily_pct_returns(data)
# print(data.head())
# print(nvda_daily_returns.head())
# print(nvda_daily_pct_returns.head())

# StockDFDataBasketPlotter().plot_all_stocks_close_prices(data_dict)
res = StockPerformanceToolkit().compute_stock_basket_daily_returns(data_dict)
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# print(res["NVDA"].head())
# print(nvda_daily_returns.head())
# StockDFDataBasketPlotter().plot_all_stocks(res)

adi_close = data_dict["ADI"]["Close"]
amd_close = data_dict["AMD"]["Close"]
intc_close = data_dict["INTC"]["Close"]
nvda_close = data_dict["NVDA"]["Close"]

collected_features = CollectAndMergeSeriesFeatures(adi_close = adi_close, amd_close = amd_close, intc_close = intc_close, nvda_close = nvda_close)
stocks_close_prices_df = collected_features.get_features_df()
stocks_close_prices_df.plot()
