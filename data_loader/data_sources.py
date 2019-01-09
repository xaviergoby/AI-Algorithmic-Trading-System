# Author: Xavier O'Rourke Goby

import pandas_datareader as web
import pandas as pd
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from pytrends.request import TrendReq
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def get_stocks_data(stock_idx = "AAPL", start_date = "01/01/2004", end_date = "12/06/2018"):
    """
    Requires the pandas-datareader library
    :param stock_idx: str of yahoo index be default is "AAPL"
    :param start_date: str with format mm/dd/YYYY  (so "%m-%d-%Y") by default is "01/01/2014"
    "left end date", "oldest date"
    :param end_date: str with format mm/dd/YYY (so "%m-%d-%Y") by default is  "12/03/2018"
    "right end date", "most recent date"
    :return: A pandas.core.frame.DataFrame with cols ['Dates', 'High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close']
    The index of the DataFrame is a pandas.core.indexes.datetimes.DatetimeIndex obj w/ the date stamp corresponding to
    row AKA "bar" of the table.
    The 'Dates' col is a pandas.core.series.Series type obj with it's elements being pandas._libs.tslibs.timestamps.Timestamp type objects
    """
    source = 'yahoo'
    data = web.DataReader(stock_idx,data_source=source, start=start_date, end=end_date)
    # wk_days = [d.strftime("%A") for d in data.index.date]
    datetime_dates_list = data.index.date.tolist()
    # data.insert(0, "WeekDays", wk_days)
    data.insert(0, "Dates", datetime_dates_list)
    # data.insert(0, "Dates", wk_days)
    return data


def get_google_trends_data(keyword, timeframe):
    """
    Requires the pytrends library
    Please visit the GitHub link for detailed explanation of the "unofficial API for Google Trends" called pytrends
    GitHub link: https://github.com/GeneralMills/pytrends
    :param keyword: a list of str format elements of the keywords to be searched
    i.e. ["Bitcoin"] or ["Debt", "Mortgage", "Financial Crisis"]
    :return: a pandas DataFrame object
    """
    pytrend_obj = TrendReq()
    pytrend_obj.build_payload(keyword, cat=0, timeframe = timeframe, geo='', gprop='')
    interest_over_time_df = pytrend_obj.interest_over_time()
    data = interest_over_time_df[keyword]
    return data


def date_transfromer(begin_date='2004-01-01',end_date=date.today(),interval_months=3):

    # To get a list of dates with a given interval and given begin and end date
    # Helpfull to transform date ranges to intervalls we can use for google

    emptylist = []

    # Get the right part of the string
    year = int(begin_date[0:4])
    month = int(begin_date[5:7])
    day = int(begin_date[8:10])

    # Use the datetime function to have an easier date calculation
    datum = datetime.date(year,month,day)
    while datum < end_date:

        # The format that the google function accepts
        rightformat = datum.strftime('%Y-%m-%d')
        emptylist.append(rightformat)

        # Add an interval to go to the next interval
        datum = datum + relativedelta(months=+interval_months)

    return emptylist



def multiple_time_frames_combiner(keyword,begin_date='2016-01-01',end_date=date.today()):
    # To combine the dates of multiple months
    # When you request the data from google, you only get daily data from 3 months intervals
    # When you want multiple years, you have to combine those 3 month slots
    # First we get a list of dates with 3 month intervals
    date_list_3m = date_transfromer(begin_date=begin_date,end_date=end_date,interval_months=1)
    date_number = 0

    # Make empty dataframe
    google_data_frame_3_months = pd.DataFrame()

    # Iterate over the list with 3 month intervals
    while date_number < len(date_list_3m) -1:
        start_date = date_list_3m[date_number]
        final_date = date_list_3m[date_number + 1]

        # Get the data in the right format for the Google function
        timeframe = '{} {}'.format(start_date, final_date)

        # Request the 3 month data
        google_data = get_google_trends_data(keyword,timeframe)

        # Add them to the dataframe in pandas style
        frames = [google_data_frame_3_months,google_data]
        google_data_frame_3_months = pd.concat(frames)

        date_number += 1

    return google_data_frame_3_months

def get_daily_and_montly_data(keyword,begin_date='2016-01-01',end_date=date.today()):

    # Combine the daily data with the monthly data
    # Get the timeframe in the right format for google (bigpicture)
    timeframe = '{} {}'.format('2004-01-01', date.today())

    # This dataframe has a 1-month interval if the begin date is 2004
    big_picture = get_google_trends_data(keyword,timeframe)
    daily_data = multiple_time_frames_combiner(keyword,begin_date=begin_date,end_date=end_date)
    return big_picture,daily_data

def merge_monthly_and_daily_data(keyword,begin_date='2016-01-01',end_date=date.today()):
    # Get the dataframes of the monthly and daily data
    big_picture, daily_data = get_daily_and_montly_data(keyword,begin_date=begin_date,end_date=end_date)

    # Make an empty dataframe to add the normalized data to
    normalized_dataframe = pd.DataFrame()

    # Get all the different years in the daily data
    years = daily_data.index.year.drop_duplicates()

    # Iterate over the years, then in those years, iterate over the months
    for year in years:
        # Select rows corresponding to the year
        big_picture_this_year = big_picture.loc[str(year)]
        daily_data_this_year = daily_data.loc[str(year)]

        # Get all the different months in the year
        months = daily_data_this_year.index.month.drop_duplicates()

        # Iterate over the months
        for month in months:

            # Select the rows with the right months, needs to be formatted
            month_value = big_picture_this_year.loc['{}-{}'.format(year, month)][keyword[0]]/100
            # Now month_value is a row, we want the value in the row
            month_value = month_value.values[0]

            # Select the rows with the right months, needs to be formatted
            daily_data_this_month = daily_data_this_year.loc['{}-{}'.format(year, month)]

            # Multiply all the dayvalues with the month value to get the relative value
            daily_data_this_month.loc[:, keyword[0]] *= month_value

            # Do some magic to get it all in a single dataframe
            frames = [normalized_dataframe, daily_data_this_month]
            normalized_dataframe = pd.concat(frames)

    return normalized_dataframe


def acces_month_from_date(date):
    month_only = date[:-12]
    return month_only

def get_google_trends_for_longer_time_period(keyword,begin_date='2016-01-01',end_date=date.today()):
    # I think this is called a wrapper?
    # This function is to make it all look a bit nicer
    normalized_dataframe = merge_monthly_and_daily_data(keyword,begin_date=begin_date,end_date=end_date)
    return normalized_dataframe