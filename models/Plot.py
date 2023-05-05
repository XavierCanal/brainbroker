import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
import logging
import pandas as pd
from pandas import json_normalize, read_json
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric
from prophet.serialize import model_to_json, model_from_json


def generate_plot_candlestick(data):
    try:
        df = pd.DataFrame(data['candlesticks'])
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
    df_cv = cross_validation(m, initial='365 days', period='100 days', horizon='165 days')
    fig = plot_cross_validation_metric(df_cv, metric='mape')
    fig.show()
    fig_json = pio.to_json(fig)
    return fig_json


def generate_forecast(data):
    df = json_to_df(data)
    logging.info("Generating forecast for data: " + str(df['ds']))
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    fig = m.plot(forecast)
    fig.show()
    fig_json = pio.to_json(fig)
    return fig_json


def json_to_df(data):
    data = pd.DataFrame(data['candlesticks'])
    df = data[['date', 'close']]
    df.rename(columns={'date': 'ds', 'close': 'y'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])
    return df
