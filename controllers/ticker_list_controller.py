import logging

from pymongo.errors import ServerSelectionTimeoutError

import utils.mongo.ticker_list as ticker


def is_updated():
    try:
        logging.info(" Checking if the tickers are updated...")
        if ticker.is_updated():
            logging.info(" The tickers are updated!!")
            return True

        logging.info(" The tickers aren't updated, updating")
        return ticker.update_tickers()
    except ServerSelectionTimeoutError:
        logging.error(" Failed to connect to the database", exc_info=True)
        return False
    except Exception:
        logging.error(" Failed to check if the tickers are updated", exc_info=True)
        return False


def ticker_exists(ticker_name):
    try:
        logging.info(" Checking if ticker %s exists", ticker)
        return ticker.find_ticker(ticker_name)
    except Exception:
        logging.error(" Failed to check if ticker exists", exc_info=True)
        return False


def get_tickers(ticker_regex=None):
    try:
        logging.info(" Getting all tickers")
        return ticker.get_tickers(ticker_regex)
    except Exception:
        logging.error(" Failed to get tickers", exc_info=True)
        return False
