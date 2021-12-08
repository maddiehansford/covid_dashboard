import requests
import json
from flask import Markup
import logging

FORMAT = '%(levelname)s: %(asctime)s: %(message)s' 
logging.basicConfig(filename='log_file.log', format=FORMAT, level=logging.INFO)

with open('config.json') as f:
    data = json.load(f)
    data = data["keys"]

def news_API_request(covid_terms:str = "Covid COVID-19 coronavirus") -> list:
    """This function creates a URL and retrives all the covid articles
    from it, returning them in a list of dictionaries.

    Args:
        covid_terms (str, optional): Terms related to coronavirus in order to
        filter through news articles. 
        Defaults to "Covid COVID-19 coronavirus".

    Returns:
        list: List of covid articles stored as dictionaries
    """
    logging.info('NEWS REQUEST')
    api_key = data["news"]
    base_url = 'https://newsapi.org/v2/everything?'
    final_url = base_url+"q="+covid_terms+"&apikey="+api_key
    covid_news = requests.get(final_url).json()
    news_articles = covid_news['articles']
    for content in news_articles:
        content['content'] = content['description'] + "  " + Markup("<a href=" + content["url"] + ">" + "Read More" + "<a>")
    return news_articles
