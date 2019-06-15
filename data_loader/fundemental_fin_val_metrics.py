import requests
from bs4 import BeautifulSoup
from configs_and_settings import stock_tickers
from configs_and_settings.settings import default_settings
from configs_and_settings import stock_tickers
from collections import defaultdict



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
        return stock_val_metrics_dict
    else:
        for val_metrix in valuation_metrics:
            results = soup.find("td", {"data-test": val_metrix})
            value = results.text
            stock_val_metrics_dict[val_metrix] = value
        return stock_val_metrics_dict


def get_company_profile_info(stock_index):
    """
    :param stock_index: an str of the stock ticker (from Yahoo), e.g. "NVDA"
    :return: a dict, e.g.
    {'company_name': 'NVIDIA Corporation', 'stock_ticker': 'NVDA', 'sector': 'Technology', 'industry_name': 'Semiconductors'}
    """
    company_profile_info_settings = default_settings["yahoo_fin_company_profile_info_html_dict"]
    stock_url = "https://finance.yahoo.com/quote/{0}/profile?p={0}&.tsrc=fin-srch".format(stock_index)
    web_page = requests.get(stock_url)
    soup = BeautifulSoup(web_page.content, "html.parser")

    company_name_html = company_profile_info_settings["company_name_html"]
    company_name_html_element = soup.find(company_name_html["html_tag"],
                                          {company_name_html["html_attr_dict"]["key"]
                                           :company_name_html["html_attr_dict"]["value"]})
    company_name = company_name_html_element.text

    main_html_element = company_profile_info_settings["main_html_element"]
    main_html_element_attrs_dict = main_html_element["html_attrs_dict"]
    keys = main_html_element_attrs_dict["keys"]
    values = main_html_element_attrs_dict["values"]
    main_html_element = soup.find(main_html_element["html_tag"],
                                  {keys[0]:values[0], keys[1]:values[1]})

    market_sector_html = company_profile_info_settings["market_sector_html"]
    sector_name = main_html_element.find(market_sector_html["html_tag"],
                                         {market_sector_html["html_attr_dict"]["key"]
                                          :market_sector_html["html_attr_dict"]["value"]}).text

    market_industry_html = company_profile_info_settings["market_industry_html"]
    industry_name = main_html_element.find(market_industry_html["html_tag"],
                                         {market_industry_html["html_attr_dict"]["key"]
                                          :market_industry_html["html_attr_dict"]["value"]}).text


    compiled_key_company_profile_infos = {"company_name":company_name,
                                          "sector": sector_name,
                                          "industry_name": industry_name}
    # conpiled_key_company_profile_infos = {"stock_ticker":stock_index,
    #                                       "company_name":company_name,
    #                                       "sector":sector_name,
    #                                       "industry_name":industry_name}

    return compiled_key_company_profile_infos


def get_multiple_stocks_fundamental_valuation_metrics(stock_index_list, valuation_metrics = None):
    """
    :param stock_index_list:
    :return: a dict of dict! Head/top dict keys are companies Yahoo finance stock tickers in str format.
    The value of each of these stock ticker keys (in str format) are dicts of their fundamental valuation metrics
    """
    multiple_stocks_val_metrics_dict = {}
    for stock_idx in stock_index_list:
        stock_val_metrics_dict = get_single_stock_fundamental_valuation_metrics(stock_idx)
        multiple_stocks_val_metrics_dict[stock_idx] = stock_val_metrics_dict
    return multiple_stocks_val_metrics_dict


def get_multiple_stocks_key_profile_info(stock_index_list):
    """
    :param stock_index: a list of the stock tickers (from Yahoo), e.g. ["NVDA", "INTC"]
    :return: a dict of nested dicts, e.g.
    {'company_name': 'NVIDIA Corporation', 'stock_ticker': 'NVDA', 'sector': 'Technology', 'industry_name': 'Semiconductors'}
    {'company_name': 'Intel Corporation', 'stock_ticker': 'INTC', 'sector': 'Technology', 'industry_name': 'Semiconductors'}
    """
    all_stocks_key_info_dict = {}
    for stock_idx in stock_index_list:
        stock_key_profile_info_dict = get_company_profile_info(stock_idx)
        all_stocks_key_info_dict[stock_idx] = stock_key_profile_info_dict
    return all_stocks_key_info_dict


def get_all_data_on_multiple_stocks(stock_index_list):
    multiple_stocks_fundemental_data_dict = get_multiple_stocks_fundamental_valuation_metrics(stock_index_list)
    multiple_stocks_key_profile_info_dict = get_multiple_stocks_key_profile_info(stock_index_list)
    all_data_on_multiple_stocks = {}
    for stock_idx in stock_index_list:
        all_data_on_multiple_stocks[stock_idx] = {**multiple_stocks_key_profile_info_dict[stock_idx],
                                                 **multiple_stocks_fundemental_data_dict[stock_idx]}
    return all_data_on_multiple_stocks





if __name__ == "__main__":
    print(stock_tickers.SEMICONDUCTOR_TICKERS)
    # fin_val_metric = ["EPS_RATIO-value"]
    # res = get_multiple_stocks_fundamental_valuation_metrics(stock_tickers.SEMICONDUCTOR_TICKERS, fin_val_metric)
    # res1 = get_multiple_stocks_fundamental_valuation_metrics(stock_tickers.SEMICONDUCTOR_TICKERS)
    # res2 = get_multiple_stocks_key_profile_info(stock_tickers.SEMICONDUCTOR_TICKERS)
    res3 = get_all_data_on_multiple_stocks(stock_tickers.SEMICONDUCTOR_TICKERS)
