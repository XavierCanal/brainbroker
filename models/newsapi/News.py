import os

import openai
import json
import logging
import pandas as pd
from datetime import datetime

openai.api_key = os.getenv('OPENAI_API_KEY')
import plotly.io as pio


def get_headlines_from_range(ticker, change_points, fig):
    """
    This function will get the headlines from the range of dates that we have in the database
    df structure ["q", "start_date", "end_date"]
    :param change_points:
    :param ticker:
    :return:
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    json_data = transform_json(change_points)
    logging.info("Getting headlines from range for " + ticker)
    message = "Respond with events and the affected value that happened between the given date ranges. " \
              "These events may have affected " + ticker \
              + ", either in terms of the company or the stock price. Please provide notable events during each " \
                "specified period. The company is  " + ticker + ", and the dates are as follows:" + json_data + \
              "\nThe format of the json of the date is: \n" \
              + "{\nstart-date : end-date\n} \n\n Respond with this format: \n\n" \
                "{\n {start-date : end-date } : {company-event: event related with the company or stock," \
                "company-event-date: Date of that event, global-event: " \
                "important event that may affect the company or stock, " \
                "global-event-date: Date of that event" \
                "company-event-affect: number (-10 to 10), global-event-affect: number (-10 to 10) }\n}\n " \
                "If you encounter any errors or cannot find any events, please fill the respective fields with an" \
                " empty string. Keep in mind that we are looking for both company-specific events and global " \
                "events that may have influenced the company or stock price, " \
                "remember to fill also the date of each event. Try to avoid events like X company price went up " \
                "we want to detect the reason why the price went up or down, not the price or value itself."
    print(message)
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "system", "content": message}])
    return chat_completion.choices[0].message.content


def stamp_news_to_plot(headlines_string, figure):
    """
    This function will stamp the news to the plot, the headlines structure is
    {
        "date": {
            "company-event": "event related with the company or stock",
            "global-event": "important event that may affect the company or stock",
            "company-event-affect": number (-10 to 10),
            "global-event-affect": number (-10 to 10)
        }
    }
    :param change_points:
    :param headlines:
    :return:
    """

    # For each headline, we will add a line to the plot
    # through the json, so we can't use a simple for loop, we have to use iteritems
    # We have to think that the date has this format "start-date : end-date" so we only have to get the start date
    # and it'll have a label with the global event - affect, and the company event - affect
    print(headlines_string)
    headline = json.loads(headlines_string)
    for date, event in headline.items():
        # We have to get the start date, so we split the string by the : and get the first element
        company_event_date = event["company-event-date"]
        global_event_date = event["global-event-date"]
        company_affect = str(event["company-event-affect"])
        global_affect = str(event["global-event-affect"])
        # Now we add the line to the plot we have to put the events inside the vline like a map
        global_event = ("<b>Global event: </b>" + event["global-event"] + "<br> Value: " + global_affect
                        + "<br> Date: " + global_event_date)
        company_event = ("<b>Company related event: </b>" + event["company-event"]
                         + "<br> Value: " + company_affect + "<br> Date: " + company_event_date)
        annotation = dict(
            x=[global_event_date, global_event_date],
            y=[figure.data[0].y.min(), figure.data[0].y.max()],
            mode="lines",
            name="Vertical Line",
            hovertemplate=global_event
        )
        annotation2 = dict(
            x=[company_event_date, company_event_date],
            y=[figure.data[0].y.min(), figure.data[0].y.max()],
            mode="lines",
            name="Vertical Line",
            hovertemplate=company_event
        )
        figure.add_trace(annotation)
        figure.add_trace(annotation2)

    figure.update_layout(template='seaborn', hovermode="closest")
    pio.show(figure)
    return


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
