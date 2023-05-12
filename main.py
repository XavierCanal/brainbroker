from flask import request, jsonify, Flask
import logging
import sys
from utils.mongo import historical
from controllers.historical_controller import get_company
from controllers.ticker_list_controller import is_updated as is_ticker_updated
from routes.company_routes import company_routes
from routes.ticker_list_routes import ticker_list_routes
from routes.binance_routes import binance_routes
from routes.plot_routes import plot_routes
from controllers import binance_controller as binance


app = Flask(__name__)

app.register_blueprint(company_routes, url_prefix='/company')
app.register_blueprint(ticker_list_routes, url_prefix='/tickerList')

# Binance api registers
app.register_blueprint(binance_routes, url_prefix='/binance')

# Plot routes
app.register_blueprint(plot_routes, url_prefix='/plot')


def setupLogger():
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return

    # Create console handler with custom formatter
    formatter = logging.Formatter('\033[32m%(levelname)s:%(message)s\033[0m')
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def checkTickers():
    """
    This function will check if the tickers are in the database, if not, it will add them
    :return:
    """
    return is_ticker_updated()


def checkSymbols():
    """
    This function will check if the symbols are in the database, if not, it will add them
    :return:
    """
    return binance.is_updated()


if __name__ == "__main__":
    from waitress import serve

    setupLogger()
    if checkTickers() and checkSymbols():
        logging.info(" 🚀🚀 Server started 🚀🚀")
        serve(app, host="0.0.0.0", port=5050)
    else:
        logging.error("❌❌ Failed to start server ❌❌")
        logging.info("💀 Stopping server... 💀")
