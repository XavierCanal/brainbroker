# -*- coding: utf-8 -*-
"""

@author: Xavier Canal
"""
import logging
import yahoo_fin.stock_info as yf
import yfinance as yf2
from datetime import datetime

from models.Candlestick import Candlestick
from models.enums.yahoo_data_restrictions import Restrictions


class Stock(Candlestick):
    def __init__(self, ticker, start_date="", end_date="", interval="ONE_DAY"):
        super().__init__(start_date, end_date, interval)
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
        return self.ticker + "-" + self.start_date.__str__() + "-" + self.end_date.__str__() + "-" + self.interval

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

            print(self.ticker, start_date, end_date, self.interval)
            stock = yf2.download(self.ticker, start=start_date, end=end_date, interval=self.interval)
            print(stock)
            return stock
        except Exception:
            logging.exception("Failed to get information, probably this ticket doesn't exist", exc_info=True)
