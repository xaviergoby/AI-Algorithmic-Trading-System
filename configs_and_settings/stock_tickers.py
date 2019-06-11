

# For some strange reason fundemental_fin_val_metrics.get_company_profile_info() throws an error when the stock index
# "ADI" is included:
# File "C:/Users/XGOBY/noname2/data_loader/fundemental_fin_val_metrics.py", line 59, in get_company_profile_info
# sector_name = main_html_element.find(market_sector_html["html_tag"],
# AttributeError: 'NoneType' object has no attribute 'find'
# SEMICONDUCTOR_TICKERS = ["INTC", "NVDA", "ADI", "QCOM", "AMD", "XLNX", "ASML", "TXN"]

# Works fine! Does not incl. "ADI" but instead incl's. "MU"
SEMICONDUCTOR_TICKERS = ["INTC", "NVDA", "MU", "QCOM", "AMD", "XLNX", "ASML", "TXN"]