import requests
import json
from flask import Markup

with open('config.json') as f:
    data = json.load(f)
    data = data["keys"]

def news_API_request(covid_terms = "Covid COVID-19 coronavirus"):
    ##creates URL
    api_key = data["news"]
    base_url = 'https://newsapi.org/v2/everything?'
    final_url = base_url+"q="+covid_terms+"&apikey="+api_key

    ##TODO : try/except
    covid_news = requests.get(final_url).json()
    news_articles = covid_news['articles']

    ## better format -> description instead of content
    ## also adds url that opens to actual article
    for content in news_articles:
        content['content'] = content['description'] + Markup("<a href=" + content["url"] + ">" + " Read More" + "<a>")
  
    return news_articles