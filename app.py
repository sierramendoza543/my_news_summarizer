import streamlit as st
import requests
from datetime import datetime
import random

# Replace with your actual Google News API Key
api_key = "91e12b0daa1e4de9b5a5a15b4bd40a81"

# List of available U.S. news sources
us_sources = [
    'abc-news', 
    'axios', 
    'bbc-news', 
    'bloomberg', 
    'breitbart-news', 
    'business-insider', 
    'cbs-news', 
    'cnn', 
    'cnn-es', 
    'fox-news', 
    'fortune', 
    'google-news', 
    'google-news-ar', 
    'google-news-au', 
    'google-news-br', 
    'google-news-ca', 
    'google-news-fr', 
    'google-news-in', 
    'google-news-is', 
    'google-news-it', 
    'google-news-ru', 
    'google-news-sa', 
    'google-news-uk', 
    'msnbc', 
    'nbc-news', 
    'newsweek', 
    'politico', 
    'reuters', 
    'the-american-conservative', 
    'the-globe-and-mail', 
    'the-hill', 
    'the-huffington-post', 
    'the-wall-street-journal', 
    'the-washington-post', 
    'the-washington-times', 
    'time', 
    'usa-today', 
    'vice-news', 
    'wired'
]

def get_news_articles(query, sources, sort_by=None):
    """Fetches news articles from the Google News API."""
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": api_key
    }

    if sources and sources != ['All']:
        params["sources"] = ",".join(sources)

    if sort_by:
        params["sortBy"] = sort_by

    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise an exception for bad status codes
    data = response.json()

    # Filter articles that don't contain "random.com" in the link
    return [article for article in data['articles'] if "random.com" not in article['url']]

def create_quiz(synopsis):
    """Creates a simple multiple-choice quiz based on the article synopsis."""
    keywords = synopsis.split() 
    possible_answers = [random.choice(keywords) for _ in range(4)] 
    correct_answer = random.choice(keywords) 
    possible_answers[random.randint(0, 3)] = correct_answer
    random.shuffle(possible_answers)
    return possible_answers, correct_answer

def display_article_and_quiz(article):
    """Displays the article and presents the quiz."""
    st.write(f"**{article['source']['name']}", f", \"{article['title']}\"")
    st.write(f"**Date:** {datetime.fromisoformat(article['publishedAt']).strftime('%Y-%m-%d')}")
    st.write(f"**Link:** {article['url']}")
    st.write(f"**Synopsis:** {article['description']}")
    st.write("---")

    synopsis = article['description']
    possible_answers, correct_answer = create_quiz(synopsis)

    st.write("**Quiz:**")
    user_answer = st.radio("Which keyword is related to the article?", possible_answers)

    if st.button("Submit"):
        if user_answer == correct_answer:
            st.success("Correct!")
        else:
            st.error("Incorrect.")

def main():
    st.title("News Article Finder & Quiz")

    query = st.text_input("Enter your research topic:")
    source_options = ['All'] + us_sources
    selected_sources = st.selectbox("Select news sources:", source_options)
