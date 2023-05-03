import logging
from datetime import datetime
import os

from flask.cli import load_dotenv

from utils.mongo.connection import DatabaseConnection
from binance.client import Client
import datetime as dt

# Get the instance of the database connection
db_client = DatabaseConnection.getInstance()

URL_TICKERS = "https://raw.githubusercontent.com/shilewenuw/get_all_tickers/master/get_all_tickers/tickers.csv"
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')


def get_symbols(symbol_regex=None):
    """
    This function will get the symbols from the database, if symbol_regex is not None, we will filter the symbols
    Because there are a lot of symbols with the same name, but with different currency like ETHBTC, ETHUSDT, ETHUSDC
    :return:
    """
    try:
        col = db_client.BrainBroker.symbols_list
        # We check if the collection exists with the index name inside the document
        if col.find_one({}):
            symbols = col.find_one({})["list"]
            if symbol_regex is not None:
                symbols = [symbol for symbol in symbols if symbol_regex in symbol]
            return symbols
        else:
            return False
    except Exception:
        logging.error("Failed to get symbols", exc_info=True)
        return False


def is_updated():
    """
    We check if exists collection, if exists we check that the date is not older than 15 day
    :param symbol:
    :return:
    """
    col = db_client.BrainBroker.symbols_list
    # First we check if the collection exists with the index name inside the document
    if col.count_documents({}) > 0:
        date = col.find_one({})["date"]
        if (dt.datetime.now() - date) > dt.timedelta(days=15):
            return False
        else:
            return True
    else:
        return False


def update_symbols():
    try:
        col = db_client.BrainBroker.symbols_list

        # First we check if the collection exists with the index name inside the document
        client = Client(api_key, api_secret)
        exchange_info = client.get_exchange_info()['symbols']
        symbols = [symbol['symbol'] for symbol in exchange_info]
        # Now we insert the df.index (array) into the collection
        col.insert_one({"date": datetime.now(), "list": symbols})

        return True
    except Exception:
        logging.error("Failed to update tickers", exc_info=True)
        return False


def symbol_exists(sy):
    """
    This function will check if the symbol exists in the database
    :param sy:
    :return:
    """
    try:
        col = db_client.BrainBroker.symbols_list
        # We check if the collection exists with the index name inside the document
        if col.find_one({}):
            symbols = col.find_one({})["list"]
            if sy in symbols:
                return True
            else:
                return False
        else:
            return False
    except Exception:
        logging.error("Failed to check if symbol exists", exc_info=True)
        return False