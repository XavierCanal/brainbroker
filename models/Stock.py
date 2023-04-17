# -*- coding: utf-8 -*-
"""

@author: Xavier Canal
"""
import logging
import yahoo_fin.stock_info as yf
import yfinance as yf2
from datetime import datetime
from models.enums.yahoo_data_restrictions import Restrictions


class Stock:
    def __init__(self, ticker, start_date, end_date, interval="ONE_DAY"):
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

    def __str__(self):
        return self.ticker + "-" + self.start_date.__str__() + "-" + self.end_date.__str__() + "-" + self.interval

    def toJSON(self):
        return {
            "ticker": self.ticker,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "interval": self.interval
        }

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

    def get(self):
        try:
            print(self.ticker, self.start_date, self.end_date, self.interval)
            stock = yf2.download(self.ticker, start=self.start_date, end=self.end_date, interval=self.interval)
            print(stock)
            return stock
        except Exception:
            logging.exception("Failed to get information, probably this ticket doesn't exist", exc_info=True)
