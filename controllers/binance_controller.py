import logging

from pymongo.errors import ServerSelectionTimeoutError

import utils.mongo.symbol_list as symbol
import models.Symbol as Symbol


def is_updated():
    try:
        logging.info(" Checking if the symbols are updated...")
        if symbol.is_updated():
            logging.info(" The symbols is updated!!")
            return True

        logging.info(" The symbols aren't updated, updating")
        return symbol.update_symbols()
    except ServerSelectionTimeoutError:
        logging.error(" Failed to connect to the database", exc_info=True)
        return False
    except Exception:
        logging.error(" Failed to check if the symbols are updated", exc_info=True)
        return False


def update_symbols():
    try:
        logging.info(" Updating symbols...")
        return symbol.update_symbols()
    except ServerSelectionTimeoutError:
        logging.error(" Failed to connect to the database", exc_info=True)
        return False
    except Exception:
        logging.error(" Failed to update symbols", exc_info=True)
        return False


def get_symbols(symbol_regex: None):
    try:
        logging.info(" Getting symbol %s", symbol_regex)
        return symbol.get_symbols(symbol_regex)
    except ServerSelectionTimeoutError:
        logging.error(" Failed to connect to the database", exc_info=True)
        return False
    except Exception:
        logging.error(" Failed to get symbols", exc_info=True)
        return False


def aggregate_symbol(sy: Symbol) -> []:
    try:
        logging.info(" Aggregating symbol %s", symbol)
        return sy.get()
    except Exception:
        logging.error(" Failed to aggregate symbol %s", symbol, exc_info=True)
        return False
