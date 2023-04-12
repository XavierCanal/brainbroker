# -*- coding: utf-8 -*-
"""

@author: Xavier Canal
"""
import logging
import yahoo_fin.stock_info as yf


def getStock(stock):
    try:
        stock = yf.get_data(stock, start_date='2014-01-01', end_date='2019-12-31')
        return stock
    except Exception:
        logging.error("Failed to get information, probably this ticket doesn't exist", exc_info=True)
