from flask import Blueprint, request, jsonify, Flask, Response, json
import logging
from datetime import datetime
from controllers import binance_controller as binance
from models.Symbol import Symbol
import pandas as pd

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
    result = []
    symbol = Symbol(request.json['Symbol'])
    logging.info(" Updating symbol %s" % symbol + "|| Start: " + str(datetime.now()))
    if not historical.stock_info_already_exists(symbol.name, symbol):
        df = binance.get_symbol(symbol, start_date, end_date, interval)
        df['data'] = df.index
        df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low',
                           'Adj Close': 'adjclose', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
        data_dict = df.to_dict('records')
        outcome = historical.aggregateSymbol(symbol, data_dict, Symbol(symbol))
        if outcome is False:
            return Response("Error", status=500, mimetype='application/json')
        result.append(outcome)
    else:
        result.append("The information of the symbol %s already exists" % symbol)
    logging.info(" End: " + str(datetime.now()))
    return result
