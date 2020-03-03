from pandas_datareader.av import AlphaVantage
from pandas_datareader.av.forex import AVForexReader
import logging
import goose3
import scrapy
import json
import statsmodels
from bs4 import BeautifulSoup
import requests
import selenium



# My Alpha Vantage API KEY: Y108UZC2YEK2VKN5
api_key = "Y108UZC2YEK2VKN5"





eur_jpy = AVForexReader(symbols="EUR/JPY", retry_count=3, pause=0.1, api_key=api_key)
