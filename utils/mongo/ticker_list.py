import logging
import pandas as pd
from datetime import datetime

from utils.mongo.connection import DatabaseConnection

# Get the instance of the database connection
db_client = DatabaseConnection.getInstance()

URL_TICKERS = "https://raw.githubusercontent.com/shilewenuw/get_all_tickers/master/get_all_tickers/tickers.csv"


def is_updated():
    col = db_client.BrainBroker.ticker_list
    # First we check if the collection exists with the index name inside the document
    if col.count_documents({}) > 0:
        return True
    else:
        return False


def update_tickers():
    try:
        col = db_client.BrainBroker.ticker_list
        # First we check if the collection exists with the index name inside the document
        df = pd.read_csv(URL_TICKERS, index_col=0)
        # Now we insert the df.index (array) into the collection
        col.insert_one({"date": datetime.now(), "list": df.index.to_list()})

        return True
    except Exception:
        logging.error("Failed to update tickers", exc_info=True)
        return False


def find_ticker(ticker_name):
    try:
        col = db_client.BrainBroker.ticker_list
        # We check if the collection exists with the index name inside the document
        if col.find_one({"list": ticker_name}):
            return True
        else:
            return False
    except Exception:
        logging.error("Failed to find ticker", exc_info=True)
        return False


def get_tickers():
    try:
        col = db_client.BrainBroker.ticker_list
        # We check if the collection exists with the index name inside the document
        if col.find_one({}):
            return col.find_one({})["list"]
        else:
            return False
    except Exception:
        logging.error("Failed to get tickers", exc_info=True)
        return False
