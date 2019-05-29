import requests
from bs4 import BeautifulSoup
from configs import stock_tickers



def get_single_stock_fundamental_valuation_metrics(stock_index_str, valuation_metrics = None):
    """
    :param stock_index_str: str of the companies corresponding Yahoo finance stock index/ticker, e.g. "NVDA" for Nvidia
    :param valuation_metrics: returns a dict with the name of the valuation metric key and the value of this as the keys corresponding value
    by def (so when valuation_metrics = None is left unchanged or no arg for valuation_metrics is provided) returns a dict with valuations
    metrics: ["EPS_RATIO-value", "PE_RATIO-value"]
    :return:
    """
    stock_url = "https://finance.yahoo.com/quote/{0}?p={0}".format(stock_index_str)
    web_page = requests.get(stock_url)
    soup = BeautifulSoup(web_page.content, "html.parser")
    def_valuation_metrics = ["EPS_RATIO-value", "PE_RATIO-value"]
    stock_val_metrics_dict = {}
    if valuation_metrics is None:
        for val_metrix in def_valuation_metrics:
            results = soup.find("td", {"data-test": val_metrix})
            value = results.text
            stock_val_metrics_dict[val_metrix] = value
            print("{0} {1}: {2}".format(stock_index_str, val_metrix, value))
        return stock_val_metrics_dict
    else:
        for val_metrix in valuation_metrics:
            results = soup.find("td", {"data-test": val_metrix})
            value = results.text
            stock_val_metrics_dict[val_metrix] = value
            print("{0} {1}: {2}".format(stock_index_str, val_metrix, value))
        return stock_val_metrics_dict


def get_multiple_stocks_fundamental_valuation_metrics(stock_index_list, valuation_metrics = None):
    """
    :param stock_index_list:
    :return: a dict of dict! Head/top dict keys are companies Yahoo finance stock tickers in str format.
    The value of each of these stock ticker keys (in str format) are dicts of their fundamental valuation metrics
    """
    multiple_stocks_val_metrics_dict = {}
    for stock_idx in stock_index_list:
        stock_val_metrics_dict = get_single_stock_fundamental_valuation_metrics(stock_idx, valuation_metrics)
        multiple_stocks_val_metrics_dict[stock_idx] = stock_val_metrics_dict
    return multiple_stocks_val_metrics_dict



if __name__ == "__main__":
    print(stock_tickers.SEMICONDUCTOR_TICKERS)
    fin_val_metric = ["EPS_RATIO-value"]
    res = get_multiple_stocks_fundamental_valuation_metrics(stock_tickers.SEMICONDUCTOR_TICKERS, fin_val_metric)
    # res = get_multiple_stocks_fundamental_valuation_metrics(stock_tickers.SEMICONDUCTOR_TICKERS)