import logging
import utils.mongo.ticker as ticker


def is_updated():
    logging.info(" Checking if the database is updated...")
    if ticker.is_updated():
        logging.info(" Database is updated!!")
        return

    logging.info(" Database is not updated, updating")
    ticker.update_tickers()
