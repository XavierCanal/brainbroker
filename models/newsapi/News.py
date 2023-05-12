import os

import numpy as np
import openai
import json

import pandas as pd
from pandas import Series
from datetime import datetime

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_headlines_from_range(ticker, change_points):
    """
    This function will get the headlines from the range of dates that we have in the database
    df structure ["q", "start_date", "end_date"]
    :param change_points:
    :param ticker:
    :return:
    """
    print(os.getenv("OPENAI_API_KEY"))
    openai.api_key = os.getenv("OPENAI_API_KEY")
    json_data = transform_json(change_points)
    print(json_data)
    return "Respond with events and the affected value that happened between the ranges given next. " \
              "For he company or in the world that may have affected " \
              "the company or the stock price. The company is " + ticker \
              + ". The dates are: \n\n" + json_data + "\nThe format of the json of the date is: \n" \
              + "{\nstart-date : end-date\n} \n\n Respond with this format: \n\n" \
                "{\n{start-date: end-date} : {company-event: event related with the company or stock, global-event: " \
                "important event that may affect the company or stock, " \
                "company-event-affect: number (-10 to 10), global-event-affect: number (0-10) }\n}\n " \
                "VERY IMPORTANT: Only send the json, if you encounter " \
                "with any error, or you can't find any event, just fill with an empty string. " \
                "Please provide notable events during each specified period. Remember that we are looking for " \
                "GLOBAL events and COMPANY events and the affect values, represent if they mau have good impact (10) " \
                "or bad impact (-10) in the company or stock."
    # chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
    #                                                messages=[{"role": "system", "content": message}])
    # return chat_completion.choices[0].message.content


def transform_json(data):
    print(data.values.tolist())

    timestamps = list(
        map((lambda x: pd.to_datetime(x, utc=True, unit='ns').strftime('%Y-%m-%d')), data.values.tolist()))

    result = {}
    for index, item in enumerate(timestamps):
        if not index == len(timestamps) - 1:
            result.update({timestamps[index]: timestamps[index + 1]})
    print(result)
    return json.dumps(result)
