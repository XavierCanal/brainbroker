from flask import Blueprint, request, jsonify, Flask, Response, json
import logging
import sys
from controllers import ticker_list_controller
import json as _json

ticker_list_routes = Blueprint('ticker_list_routes', __name__)


@ticker_list_routes.route('/getTickers', methods=['GET'])
def get_tickers():
    return ticker_list_controller.get_tickers()


@ticker_list_routes.route('/getTickers', defaults={'symbol_regex': None})
@ticker_list_routes.route('/getTickers/<string:symbol_regex>', methods=['GET'])
def get_symbols(symbol_regex=None):
    """
    :param symbol_regex: This is the regex that we will use to filter the symbols
    This function will update the companies in the database, using yahoo finances, we use get_data, that
    gives us the data from the company from x year to y year with intervals of 1 day
    :return:
    """
    result = ticker_list_controller.get_tickers(symbol_regex)
    if result:
        return Response(json.dumps(result), status=200, mimetype='application/json')
    elif not result:
        return Response(json.dumps(result), status=500, mimetype='application/json')
    else:
        return Response(json.dumps(result), status=404, mimetype='application/json')
