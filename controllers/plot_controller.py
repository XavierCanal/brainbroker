import logging
from controllers import historical_controller
from models import Plot
from models.newsapi import News


def get_plot(ticker, interval):
    hist = historical_controller.get_company_interval(ticker, interval)
    if not hist or hist is False:
        return "Error, company not found"
    fig_json = Plot.generate_plot_candlestick(hist)
    return fig_json


def get_plot_forecast_components(ticker, interval):
    hist = historical_controller.get_company_interval(ticker, interval)
    if not hist:
        return "Error, company not found"
    fig_json = Plot.generate_forecast_components(hist)
    return fig_json


def generate_cross_validation_forecast(ticker, interval):
    hist = historical_controller.get_company_interval(ticker, interval)
    if not hist:
        return "Error, company not found"
    fig_json = Plot.generate_cross_validation_forecast(hist)
    return fig_json


def generate_forecast(ticker, interval):
    hist = historical_controller.get_company_interval(ticker, interval)
    if not hist:
        return "Error, company not found"
    fig_json = Plot.generate_forecast(hist)
    return fig_json


def get_changepoints(ticker, interval, change_points):
    hist = historical_controller.get_company_interval(ticker, interval)
    if not hist:
        return "Error, company not found"
    fig_json = Plot.get_changepoints(hist, change_points)
    return fig_json


def get_changepoints_with_news(ticker, interval, change_points):
    hist = historical_controller.get_company_interval(ticker, interval)
    if not hist:
        return "Error, company not found"
    m, change_points = Plot.get_changepoints_with_news(hist, change_points)
    articles = News.get_headlines_from_range(ticker, change_points)
    return articles
