from flask import Blueprint, request, jsonify, Flask, Response, json
import logging
from datetime import datetime, timedelta
from controllers import binance_controller as binance
from models.Stock import Stock
import pandas as pd

from models.enums.yahoo_data_restrictions import Restrictions
from utils.mongo import historical

binance_routes = Blueprint('binance_routes', __name__)
base_url = "https://api.binance.com/api/v3"


@binance_routes.route('/getSymbols', defaults={'symbol_regex': None})
@binance_routes.route('/getSymbols/<string:symbol_regex>', methods=['GET'])
def get_symbols(symbol_regex=None):
    """
    :param symbol_regex: This is the regex that we will use to filter the symbols
    This function will update the companies in the database, using yahoo finances, we use get_data, that
    gives us the data from the company from x year to y year with intervals of 1 day
    :return:
    """
    result = binance.get_symbols(symbol_regex);
    if result:
        return Response(json.dumps(result), status=200, mimetype='application/json')
    elif not result:
        return Response(json.dumps(result), status=500, mimetype='application/json')
    else:
        return Response(json.dumps(result), status=404, mimetype='application/json')


@binance_routes.route('/aggregateSymbol', methods=['POST'])
def aggregate_symbol():
    """
    :param symbol: Symbol to update
    This function will update the companies in the database, using binance, we use aggregate_symbol, that
    gives us the data from the company from x year to y year with intervals of 1 day
    """
    if binance.symbol_exists(request.json['ticker']) is False:
        return Response("Error, empty request json or symbol doesn't exist", status=400, mimetype='application/json')
    result = []
    symbol = Stock(request.json['ticker'], request.json['start_date'], request.json['end_date'], request.json['interval'])
    logging.info(" Updating symbol %s" % symbol + "|| Start: " + str(datetime.now()))
    if not historical.stock_info_already_exists(symbol.ticker, symbol):
        df = binance.get_symbol(symbol)
        if df is None or df.empty:
            return Response("Error, empty response", status=500, mimetype='application/json')
        else:
            df['date'] = df.index
            data_dict = df.to_dict('records')
            outcome = historical.aggregateCompany(symbol.ticker, data_dict, symbol)
            if outcome is False:
                return Response("Error", status=500, mimetype='application/json')
            result.append(outcome)
    else:
        result.append("The information of the symbol %s already exists" % symbol)
    logging.info(" End: " + str(datetime.now()))
    return result


@binance_routes.route('/aggregateAllHistoricalSymbol', methods=['POST'])
def aggregateAllHistoricalSymbol():
    """
    This function will update all the companies in the database, using yahoo finances, we use get_data, that
    gives us the data from the company from x year to y year with intervals of 1 day
    :return:
    """
    result = []
    symbol = request.json['ticker']
    interval = request.json['interval']
    logging.info(" Updating symbol %s" % symbol + "|| Start: " + str(datetime.now()))
    if not binance.symbol_exists(symbol):
        return Response("Error, empty request json or symbol doesn't exist", status=400, mimetype='application/json')
    st = Stock(symbol)

    if historical.stock_info_already_exists(symbol, st):
        result.append("The information of the company %s already exists" % symbol)
        logging.info("The information of the company %s already exists" % symbol)
    else:
        if request.json['start_date'] is not None:
            print("Start date: %s" % request.json['start_date'])
            st.set_start_date(datetime.strptime(request.json['start_date'], '%Y-%m-%d'))
            st.set_end_date(Restrictions[interval].get_interval_end_date(st.start_date))
        else:
            print("no start date")
            start_date = st.get_binance_symbol().index[0]
            st.set_start_date(start_date)
            st.set_end_date(Restrictions[interval].get_interval_end_date(start_date))
        st.set_interval(Restrictions[interval].value["key"])

        logging.info("Updating company %s with start date %s, end date %s and interval %s" %
                     (symbol, st.start_date, st.end_date, st.interval))

        start_date = st.start_date
        today = datetime.now()
        while start_date < today:
            print("Start date: %s, end date: %s" % (start_date, st.end_date))
            df = st.get_binance_symbol(start_date, st.end_date)
            if df is None or df.empty:
                return Response("Error, empty response", status=500, mimetype='application/json')
            else:
                df['date'] = df.index
                data_dict = df.to_dict('records')
                historical.aggregateCompanyCollection(st.ticker, data_dict, st)
                start_date = st.end_date
                st.end_date = Restrictions[interval].get_interval_end_date(start_date)

        result.append("The information of the company %s was updated" % symbol)
    logging.info(" End: " + str(datetime.now()))

    return result


@binance_routes.route('/updateCompletedStatus', methods=['POST'])
def update_completed_status():
    """
    This function will update the completed status of the company
    :return:
    """
    result = []
    symbol = request.json['ticker']
    if not binance.symbol_exists(symbol):
        return Response("Error, empty request json or symbol doesn't exist", status=400, mimetype='application/json')

    if historical.update_completed_status(symbol):
        result.append("The information of the company %s was updated" % symbol)
    else:
        result.append("The information of the company %s was not updated" % symbol)

    return result
