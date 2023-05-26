import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
import logging
import pandas as pd
from pandas import json_normalize, read_json
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric, add_changepoints_to_plot, plot_plotly
from prophet.serialize import model_to_json, model_from_json


def generate_plot_candlestick(data):
    try:
        df = pd.DataFrame(data['candlesticks'])
        print("df: ", df)
        fig = go.Figure(data=[go.Candlestick(x=df['date'],
                                             open=df['open'],
                                             high=df['high'],
                                             low=df['low'],
                                             close=df['close'])])
        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.show()
        fig_json = pio.to_json(fig)
        return fig_json
    except Exception as e:
        logging.error("Error generating plot candlestick: " + str(e))
        return "Error generating plot candlestick: " + str(e)


def generate_plot_line(data):
    df = pd.DataFrame(data['candlesticks'])
    df['date'] = pd.to_datetime(df['date'])
    logging.info("Generating plot line for data: " + str(df['date']))
    fig = go.Figure(data=go.Scatter(x=df['date'], y=df['close']))
    fig.show()
    fig_json = pio.to_json(fig)
    return fig_json


def generate_forecast_components(data):
    data = pd.DataFrame(data['candlesticks'])
    df = data[['date', 'close']]
    df.rename(columns={'date': 'ds', 'close': 'y'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])
    logging.info("Generating forecast components for data: " + str(df['ds']))
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    fig = m.plot_components(forecast)
    fig.show()
    return model_to_json(m)


def generate_cross_validation_forecast(data):
    df = json_to_df(data)
    logging.info("Generating cross validation forecast for data: " + str(df['ds']))
    m = Prophet()
    m.fit(df)
    df_cv = cross_validation(m, initial='365 days', period='30 days', horizon='90 days')
    fig = plot_cross_validation_metric(df_cv, metric='mape')
    fig.show()
    return model_to_json(m)


def generate_forecast(data):
    df = json_to_df(data)
    logging.info("Generating forecast for data: " + str(df['ds']))
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    fig = plot_plotly(m, forecast)
    fig.update_layout(template='seaborn')
    pio.show(fig)
    
    return model_to_json(m)


def get_changepoints(data, change_points=15):
    df = json_to_df(data)
    logging.info("Getting changepoints for data: " + str(df['ds']))
    m = Prophet(seasonality_mode='multiplicative', yearly_seasonality=4, n_changepoints=change_points)
    m.fit(df)
    forecast = m.predict()
    fig = m.plot(forecast)
    add_changepoints_to_plot(fig.gca(), m, forecast)
    plt.show()
    return model_to_json(m)


def get_changepoints_with_news(data, change_points=15):
    df = json_to_df(data)
    logging.info("Getting changepoints with news for data: " + str(df['ds']))
    m = Prophet(seasonality_mode='multiplicative', changepoint_range=1, changepoint_prior_scale=0.01,
                n_changepoints=change_points)
    m.add_country_holidays(country_name='US')
    m.fit(df)
    forecast = m.predict()
    fig = m.plot(forecast)
    add_changepoints_to_plot(fig.gca(), m, forecast)
    fig = plot_plotly(m, forecast)
    plt.show()
    return fig, m.changepoints


def json_to_df(data):
    data = pd.DataFrame(data['candlesticks'])
    df = data[['date', 'close']]
    df.rename(columns={'date': 'ds', 'close': 'y'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])
    return df
