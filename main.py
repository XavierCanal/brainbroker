from flask import request, jsonify, Flask
import logging
import sys
from utils.mongo import historical
from controllers.historical_controller import get_company
from controllers.ticker_controller import is_updated as is_ticker_updated
from models.Stock import Stock
from datetime import datetime

app = Flask(__name__)


@app.route('/aggregateCompanies', methods=['POST'])
def update_companies():
    """
    :param tickers: List of companies to update
    This function will update the companies in the database, using yahoo finances, we use get_data, that
    gives us the data from the company from x year to y year with intervals of 1 day
    :return:
    """
    result = []
    for company in request.json['tickers']:
        logging.info(" Updating company %s" % company + "|| Start: " + str(datetime.now()))

        st = Stock(company)
        if historical.stock_info_already_exists(company, st):
            result.append("The information of the company %s already exists" % company)
        else:
            df = st.get()
            df['data'] = df.index
            df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low',
                               'Adj Close': 'adjclose', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
            data_dict = df.to_dict('records')

            result.append(historical.aggregateCompany(company, data_dict, st))
        logging.info(" End: " + str(datetime.now()))
    return result


@app.route('/getCompany/<string:name>', methods=['GET'])
def get_company_by_name(name):
    return get_company(name)


@app.route('/aggregateCustomCompanies', methods=['POST'])
def aggregateCompaniesWithCustomFilter():
    """
    :param tickers: List of companies to update
    :param start-date: Start date of the data
    :param end-date: End date of the data
    :param interval : Interval of time to get the data (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)

    source: https://stackoverflow.com/questions/61976027/scraping-yahoo-finance-at-regular-intervals
    source: https://www.qmr.ai/wp-content/uploads/2022/08/image-23.png
    :return:
    """
    result = []
    for ticker in request.json['tickers']:
        logging.info(" Updating company %s" % ticker + "|| Start: " + str(datetime.now()))
        st = Stock(ticker, request.json['start_date'], request.json['end_date'], request.json['interval'])
        if historical.stock_info_already_exists(ticker, st):
            result.append("The information of the company %s already exists" % ticker)
            logging.info("The information of the company %s already exists" % ticker)
        elif not st.validRange():
            result.append(
                "The information of the company %s was not updated because the date range is not valid" % ticker)
        else:
            df = st.get()
            if df.empty:
                result.append("The information of the company %s was not updated because the data is empty" % ticker)
                continue
            df['data'] = df.index
            data_dict = df.to_dict('records')
            historical.aggregateCompany(ticker, data_dict, st)

            result.append("The information of the company %s was updated" % ticker)
        logging.info(" End: " + str(datetime.now()))
    return result


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
