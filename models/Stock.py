# -*- coding: utf-8 -*-
"""

@author: Xavier Canal
"""
import logging
import yahoo_fin.stock_info as yf


class Stock:
    def __init__(self, ticker, start_date=None, end_date=None, interval="1d"):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval

    def __str__(self):
        return self.ticker + "-" + self.start_date + "-" + self.end_date + "-" + self.interval

    def toJSON(self):
        return {
            "ticker": self.ticker,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "interval": self.interval
        }

    def get(self):
        try:
            stock = yf.get_data(self.ticker, start_date=self.start_date, end_date=self.end_date, interval=self.interval)
            return stock
        except Exception:
            logging.exception("Failed to get information, probably this ticket doesn't exist", exc_info=True)
