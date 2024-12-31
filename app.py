import streamlit as st
import requests
from datetime import datetime


# Google News API Key (Replace with your actual key)
api_key = "91e12b0daa1e4de9b5a5a15b4bd40a81"

# List of available news sources (excluding removed.com)
news_sources = [
    source for source in [
        'abc-news', 'abc-news-au', 'aftenposten', 'al-jazeera-english', 'ansa', 'argaam', 'ars-technica', 
        'ary-news', 'associated-press', 'australian-financial-review', 'axios', 'bbc-news', 'bbc-sport', 
        'bild', 'blasting-news-br', 'bleacher-report', 'bloomberg', 'breitbart-news', 'business-insider', 
        'buzzfeed', 'cbc-news', 'cbs-news', 'cnn', 'cnn-es', 'crypto-coins-news', 'der-tagesspiegel', 
        'die-zeit', 'el-mundo', 'engadget', 'entertainment-weekly', 'espn', 'espn-cric-info', 'financial-post', 
        'focus', 'football-italia', 'fortune', 'four-four-two', 'fox-news', 'fox-sports', 'globo', 
        'google-news', 'google-news-ar', 'google-news-au', 'google-news-br', 'google-news-ca', 
        'google-news-fr', 'google-news-in', 'google-news-is', 'google-news-it', 'google-news-ru', 
        'google-news-sa', 'google-news-uk', 'goteborgs-posten', 'gruenderszene', 'hacker-news', 
        'handelsblatt', 'ign', 'il-sole-24-ore', 'independent', 'infobae', 'info-money', 'la-gaceta', 
        'la-nacion', 'la-repubblica', 'le-monde', 'lenta', 'lequipe', 'les-echos', 'liberation', 
        'marca', 'mashable', 'medical-news-today', 'msnbc', 'mtv-news', 'mtv-news-uk', 'national-geographic', 
        'national-review', 'nbc-news', 'news24', 'new-scientist', 'news-com-au', 'newsweek', 
        'new-york-magazine', 'next-big-future', 'nfl-news', 'nhl-news', 'nrk', 'politico', 
        'polygon', 'rbc', 'recode', 'reddit-r-all', 'reuters', 'rt', 'rte', 'rtl-nieuws', 'sabq', 
        'spiegel-online', 'svenska-dagbladet', 't3n', 'talksport', 'techcrunch', 'techcrunch-cn', 
        'techradar', 'the-american-conservative', 'the-globe-and-mail', 'the-hill', 'the-hindu', 
        'the-huffington-post', 'the-irish-times', 'the-jerusalem-post', 'the-lad-bible', 'the-next-web', 
        'the-sport-bible', 'the-times-of-india', 'the-verge', 'the-wall-street-journal', 
        'the-washington-post', 'the-washington-times', 'time', 'usa-today', 'vice-news', 'wired', 
        'wired-de', 'wirtschafts-woche', 'xinhua-net', 'ynet'
    ] if source != 'removed.com'
]

def get_news_articles(query, sources, sort_by=None):
    """Fetches news articles from the Google News API."""
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sources": ",".join(sources),
        "apiKey": api_key
    }

    if sort_by:
        params["sortBy"] = sort_by

    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise an exception for bad status codes
    data = response.json()

    return data['articles']

def display_articles(articles):
    """Displays articles in the specified format."""
    for article in articles[:5]:  # Fix indentation for the loop
        st
