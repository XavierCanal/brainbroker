from flask import request, jsonify, Flask
import logging
import sys
from get_stock import *
from utils.mongo.historical import aggregateCompany
from controllers.historical_controller import get_company

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/aggregateCompanies', methods=['POST'])
def update_companies():
    """
    :param companies: List of companies to update
    This function will update the companies in the database, using yahoo finances, we use get_data, that
    gives us the data from the company from x year to y year with intervals of 1 day
    :return:
    """
    for company in request.json['companies']:
        df = getStock(company)
        df['data'] = df.index
        data_dict = df.to_dict('records')
        return aggregateCompany(company, data_dict)


@app.route('/aggregateCustomCompanies', methods=['GET'])
def get_company_by_name():
    """
    :arg tickers: List of companies to update
    :arg period: Period of time to get the data (1d, 1wk, 1mo)
    :arg interval : Interval of time to get the data (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
    :arg group_by : Group by (ticker, column)
    :arg auto_adjust : Auto adjust (true, false)
    :arg prepost : Pre post (true, false)
    :arg threads : Threads (True/False/Integer)
    :arg proxy : Proxy url

    source: https://stackoverflow.com/questions/61976027/scraping-yahoo-finance-at-regular-intervals
    :return:
    """
    return "I see the arguments!  --->  " + request.args.get('tickers') + " " + request.args.get('period') + " " + request.args.get('interval')


@app.route('/aggregateCompanies/<string:period>', methods=['POST'])


def setupLogger():
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create console handler with custom formatter
    formatter = logging.Formatter('\033[32m%(levelname)s:%(message)s\033[0m')
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


if __name__ == "__main__":
    from waitress import serve
    setupLogger()
    logging.info("🚀🚀 Server started 🚀🚀")
    serve(app, host="0.0.0.0", port=5050)
    logging.info("💀 Stoping server... 💀")

