from flask import Blueprint, request, jsonify, Flask, Response
import logging
import sys

from models.enums.yahoo_data_restrictions import Restrictions
from utils.mongo import historical
from controllers.historical_controller import get_company
from controllers.ticker_list_controller import ticker_exists
from models.Stock import Stock
from datetime import datetime, timedelta

company_routes = Blueprint('company_routes', __name__)


@company_routes.route('/aggregateCompanies', methods=['POST'])
def update_companies():
    """
    :param tickers: List of companies to update
    This function will update the companies in the database, using yahoo finances, we use get_data, that
    gives us the data from the company from x year to y year with intervals of 1 day
    :return:
    """
    result = []
    for ticker in request.json['tickers']:
        if not ticker_exists(ticker):
            result.append("The ticker %s does not exist" % ticker)
            continue
        logging.info(" Updating ticker %s" % ticker + "|| Start: " + str(datetime.now()))

        st = Stock(ticker)
        if historical.stock_info_already_exists(ticker, st):
            result.append("The information of the ticker %s already exists" % ticker)
        else:
            df = st.get()
            df['data'] = df.index
            df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low',
                               'Adj Close': 'adjclose', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
            data_dict = df.to_dict('records')
            outcome = historical.aggregateCompany(ticker, data_dict, st)
            if outcome is False: return Response("Error", status=500, mimetype='application/json')
            result.append(outcome)
        logging.info(" End: " + str(datetime.now()))
    return result


@company_routes.route('/getCompany/<string:name>', methods=['GET'])
def get_company_by_name(name):
    return get_company(name)


@company_routes.route('/aggregateCustomCompanies', methods=['POST'])
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
        if not ticker_exists(ticker):
            result.append("The company %s does not exist" % ticker)
            continue

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
            df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low',
                               'Adj Close': 'adjclose', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
            data_dict = df.to_dict('records')
            historical.aggregateCompany(ticker, data_dict, st)

            result.append("The information of the company %s was updated" % ticker)
        logging.info(" End: " + str(datetime.now()))
    return result


@company_routes.route('/aggregateAllHistorical', methods=['POST'])
def aggregateAllHistorical():
    """
    This function will update all the companies in the database, using yahoo finances, we use get_data, that
    gives us the data from the company from x year to y year with intervals of 1 day
    :return:
    """
    result = []
    for ticker in request.json['tickers']:
        if not ticker_exists(ticker):
            result.append("The company %s does not exist" % ticker)
            continue
        logging.info(" Updating company %s" % ticker + " || Start: " + str(datetime.now()))
        st = Stock(ticker)
        if historical.stock_info_already_exists(ticker, st):
            result.append("The information of the company %s already exists" % ticker)
            logging.info("The information of the company %s already exists" % ticker)
        else:
            st.set_start_date(Restrictions[request.json['interval']].get_datetime_delta())
            st.set_interval(Restrictions[request.json['interval']].value["key"])

            logging.info("Updating company %s with start date %s, end date %s and interval %s" %
                         (ticker, st.start_date, st.end_date, st.interval))

            start_date = st.start_date

            while start_date < st.end_date:
                end_date = start_date + timedelta(days=730)
                print("Start date: %s, end date: %s" % (start_date, end_date))
                df = st.get(start_date, end_date)
                df['data'] = df.index
                df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low',
                                   'Adj Close': 'adjclose', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
                data_dict = df.to_dict('records')
                historical.aggregateCompany(ticker, data_dict, st)
                start_date = end_date

            result.append("The information of the company %s was updated" % ticker)
        logging.info(" End: " + str(datetime.now()))
    return result
