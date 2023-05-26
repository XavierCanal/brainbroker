import os
import datetime
import openai
import json
import logging
import pandas as pd
from plotly.utils import PlotlyJSONEncoder
import requests
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))


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
    figure_json = json.dumps(figure, cls=PlotlyJSONEncoder)
    return figure_json


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


def get_recent_news(q):
    top_related_headlines = newsapi.get_top_headlines(q=q,
                                                      category='business',
                                                      language='en')
    if top_related_headlines.get("totalResult") is not None:
        return json.dumps(top_related_headlines.get("articles"))

    top_related_headlines = newsapi.get_everything(q=q,
                                                   language='en',
                                                   page_size=10,
                                                   from_param=(datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'),
                                                   to=datetime.datetime.today().strftime('%Y-%m-%d')
                                                   )
    return json.dumps(top_related_headlines)


def get_headlines_evaluation(articles, ticker):
    """
    This function will get the headlines and will valuate them
    article json example:
    {
                "source": {
                "id": null,
                "name": "Hackaday"
            },
            "author": "Joseph Long",
            "title": "Early Computer Art from the 1950s and 1960s",
            "description": "Modern day computer artist, [Amy Goodchild] surveys a history of Early Computer Art from the 1950s and 1960s. With so much attention presently focused on AI-generated artwork, we should remember …read more",
            "url": "https://hackaday.com/2023/05/19/early-computer-art-from-the-1950s-and-1960s/",
            "urlToImage": "https://hackaday.com/wp-content/uploads/2023/05/Early-Computer-Art.png",
            "publishedAt": "2023-05-19T23:00:08Z",
            "content": "Modern day computer artist, [Amy Goodchild] surveys a history of Early Computer Art from the 1950s and 1960s. With so much attention presently focused on AI-generated artwork, we should remember that… [+2182 chars]"
    }
    we take the title and the description and we valuate them, then we return the valuated articles
    we expect from gpt the following structure:
    {
        "title":value
    }
    This value will go from -10 to 10, being -10 a very negative event, 0 a neutral event and 10 a very positive event
    :param articles:
    :return:
    """
    # We will create a list of the titles and descriptions
    articles = json.loads(articles)
    json_str = "{"
    for article in articles["articles"]:
        json_str += "'article': { \n title: " + article["title"] + "'description: '" + article["description"] + "},"
    json_str += "}"

    # We prepare the message with the explanation of what should gpt do
    message = "Please evaluate the potential impact of the following news articles on " + ticker + ". Assign a value between -10 " \
              "and 10 to each article based on its title and description. If you're unable to assess the article's impact," \
              "you can assign a value of 0. Please provide the response in the following format:" \
                "{'article_title': value, 'conclusion': (conclusion text)} where value is a number between -10 and 10."\
                "Please note that I am specifically " \
                "interested in evaluating the impact of these articles on IBM and not on any other company or industry." \
                "remember, the only response must be a json, nothing more."\
                "Thank you! \nArticles: \n" + json_str
    print(message)
    # We send the message to gpt and we get the response
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "system", "content": message}])
    return chat_completion.choices[0].message.content