import logging

from pymongo.errors import ServerSelectionTimeoutError

import utils.mongo.ticker as ticker


def is_updated():
    try:
        logging.info(" Checking if the database is updated...")
        if ticker.is_updated():
            logging.info(" Database is updated!!")
            return True

        logging.info(" Database is not updated, updating")
        ticker.update_tickers()
    except ServerSelectionTimeoutError:
        logging.error(" Failed to connect to the database", exc_info=True)
        return False
    except Exception:
        logging.error(" Failed to check if the database is updated", exc_info=True)
        return False
