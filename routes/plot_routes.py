from flask import Blueprint, request, jsonify, Flask, Response
import logging
import sys
from controllers import plot_controller

plot_routes = Blueprint('plot_routes', __name__)


@plot_routes.route('/getPlot', methods=['POST'])
def get_plot():
    try:
        stock, interval = request.json['stock'], request.json['interval']
        if not stock or not interval:
            return Response("Error, empty request json or symbol doesn't exist", status=400, mimetype='application/json')
        result = plot_controller.get_plot(stock, interval)
        return Response(result, status=200, mimetype='application/json')
    except Exception as e:
        logging.error("Error in get_plot: " + str(e))
        return Response("Error in get_plot: " + str(e), status=500, mimetype='application/json')


@plot_routes.route('/getPlotForecastComponents', methods=['POST'])
def get_plot_forecast_components():
    try:
        stock, interval = request.json['stock'], request.json['interval']
        if not stock or not interval:
            return Response("Error, empty request json or symbol doesn't exist", status=400, mimetype='application/json')
        result = plot_controller.get_plot_forecast_components(stock, interval)
        return Response(result, status=200, mimetype='application/json')
    except Exception as e:
        logging.error("Error in get_plot_forecast_components: " + str(e))
        return Response("Error in get_plot_forecast_components: " + str(e), status=500, mimetype='application/json')


@plot_routes.route('/generateCrossValidationForecast', methods=['POST'])
def generate_cross_validation_forecast():
    try:
        stock, interval = request.json['stock'], request.json['interval']
        if not stock or not interval:
            return Response("Error, empty request json or symbol doesn't exist", status=400, mimetype='application/json')
        result = plot_controller.generate_cross_validation_forecast(stock, interval)
        return Response(result, status=200, mimetype='application/json')
    except Exception as e:
        logging.error("Error in generate_cross_validation_forecast: " + str(e))
        return Response("Error in generate_cross_validation_forecast: " + str(e), status=500, mimetype='application/json')


@plot_routes.route('/generateForecast', methods=['POST'])
def generate_forecast():
    try:
        stock, interval = request.json['stock'], request.json['interval']
        if not stock or not interval:
            return Response("Error, empty request json or symbol doesn't exist", status=400, mimetype='application/json')
        result = plot_controller.generate_forecast(stock, interval)
        return Response(result, status=200, mimetype='application/json')
    except Exception as e:
        logging.error("Error in generate_forecast: " + str(e))
        return Response("Error in generate_forecast: " + str(e), status=500, mimetype='application/json')