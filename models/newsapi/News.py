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
    message = "Respond with events and the affected value that happened between the given date ranges. " \
           "These events may have affected" + ticker \
        + ", either in terms of the company or the stock price. Please provide notable events during each " \
          "specified period. The company is  " + ticker + ", and the dates are as follows:" + json_data + \
        "\nThe format of the json of the date is: \n" \
        + "{\nstart-date : end-date\n} \n\n Respond with this format: \n\n" \
          "{\n{start-date: end-date} : {company-event: event related with the company or stock, global-event: " \
          "important event that may affect the company or stock, " \
          "company-event-affect: number (-10 to 10), global-event-affect: number (-10 to 10) }\n}\n " \
          "If you encounter any errors or cannot find any events, please fill the respective fields with an" \
          " empty string. Keep in mind that we are looking for both company-specific events and global " \
          "events that may have influenced the company or stock price."
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "system", "content": message}])
    return chat_completion.choices[0].message.content


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
