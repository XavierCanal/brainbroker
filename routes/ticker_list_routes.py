from flask import Blueprint, request, jsonify, Flask
import logging
import sys
from controllers import ticker_list_controller

ticker_list_routes = Blueprint('ticker_list_routes', __name__)


@ticker_list_routes.route('/getTickers', methods=['GET'])
def get_tickers():
    return ticker_list_controller.get_tickers()