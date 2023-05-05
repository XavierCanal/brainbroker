# -*- coding: utf-8 -*-
"""

@author: Xavier Canal
"""
import logging

import pandas as pd
import yahoo_fin.stock_info as yf
import yfinance as yf2
from datetime import datetime
import math
from binance.client import Client

from models.enums.yahoo_data_restrictions import Restrictions


class Stock:
    def __init__(self, ticker, start_date="", end_date="", interval="ONE_DAY"):
        self.ticker = ticker
        if end_date == "":
            self.end_date = datetime.today()
        else:
            self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        if start_date == "":
            self.start_date = Restrictions[interval].get_datetime_delta()
        else:
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.interval = Restrictions[interval].value["key"]
        self.interval_enum = interval

    # TODO: Fix this class extending Candlestick, and make it work with the new Candlestick class
    # Maybe we can use the same class for both stocks and crypto
    # and we need to unify the way we get the data from yahoo finance and binance

    def __str__(self):
        return self.ticker + " - " + self.start_date.__str__() + " - " + self.end_date.__str__() + " - " + self.interval

    def set_end_date(self, end_date):
        self.end_date = end_date

    def set_start_date(self, start_date):
        self.start_date = start_date

    def set_interval(self, interval):
        self.interval = interval

    def toJSON(self):
        return {
            "ticker": self.ticker,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "interval": self.interval
        }

    """
    This function will check if the stock is valid
    @:returns True if the stock is valid, False otherwise
    """

    def validRange(self):
        try:
            logging.info("Validating range")
            # We check if start date is before end date and if the
            # time between dates is valid using the Restrictions enum
            delta = self.end_date - self.start_date
            print(self.start_date > self.end_date)
            if self.start_date > self.end_date or (delta.days > Restrictions[self.interval_enum].value["days"]):
                return False
            return True
        except Exception:
            logging.exception("Failed to validate range", exc_info=True)
            return False

    """
    This function will get the stock information from yahoo finance
    @:returns a pandas dataframe with the stock information
    """

    def get(self, start_date=None, end_date=None):
        try:
            if start_date is None:
                start_date = self.start_date
            if end_date is None:
                end_date = self.end_date
            logging.info(" ticker: %s, start_date: %s, end_date: %s, interval: %s", self.ticker, start_date, end_date, self.interval)
            stock = yf2.download(self.ticker, start=start_date, end=end_date, interval=self.interval)
            print(stock)
            return stock
        except Exception:
            logging.exception("Failed to get information, probably this ticket doesn't exist", exc_info=True)

    def get_binance_symbol(self, start_date=None, end_date=None):
        client = Client()
        if start_date and end_date:
            outcome = client.get_historical_klines(self.ticker, self.interval, start_date.strftime("%d %b %Y %H:%M:%S"), end_date.strftime("%d %b %Y %H:%M:%S"))
        else:
            outcome = client.get_historical_klines(self.ticker, self.interval, self.start_date.strftime("%d %b %Y %H:%M:%S"), self.end_date.strftime("%d %b %Y %H:%M:%S"))
        if len(outcome) == 0:
            return None
        data = pd.DataFrame(outcome)
        data.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
        data.index = [datetime.fromtimestamp(x / 1000.0) for x in data.close_time]
        return data
