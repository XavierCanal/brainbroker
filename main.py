from flask import request, jsonify, Flask
import logging
import sys
from utils.mongo import historical
from controllers.historical_controller import get_company
from controllers.ticker_controller import is_updated as is_ticker_updated
from routes.company_routes import company_routes

app = Flask(__name__)

app.register_blueprint(company_routes)


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


if __name__ == "__main__":
    from waitress import serve

    setupLogger()
    if checkTickers():
        logging.info("🚀🚀 Server started 🚀🚀")
        serve(app, host="0.0.0.0", port=5050)
    else:
        logging.error("❌❌ Failed to start server ❌❌")
        logging.info("💀 Stopping server... 💀")
