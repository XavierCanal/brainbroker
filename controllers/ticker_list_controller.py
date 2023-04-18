import logging

from pymongo.errors import ServerSelectionTimeoutError

import utils.mongo.ticker_list as ticker


def is_updated():
    try:
        logging.info(" Checking if the database is updated...")
        if ticker.is_updated():
            logging.info(" Database is updated!!")
            return True

        logging.info(" Database is not updated, updating")
        return ticker.update_tickers()
    except ServerSelectionTimeoutError:
        logging.error(" Failed to connect to the database", exc_info=True)
        return False
    except Exception:
        logging.error(" Failed to check if the database is updated", exc_info=True)
        return False


def ticker_exists(ticker_name):
    try:
        logging.info(" Checking if ticker %s exists", ticker)
        return ticker.find_ticker(ticker_name)
    except Exception:
        logging.error(" Failed to check if ticker exists", exc_info=True)
        return False


def get_tickers():
    try:
        logging.info(" Getting all tickers")
        return ticker.get_tickers()
    except Exception:
        logging.error(" Failed to get tickers", exc_info=True)
        return False
