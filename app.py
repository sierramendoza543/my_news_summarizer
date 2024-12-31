import streamlit as st
import requests
from datetime import datetime

# Google News API Key (Replace with your actual key)
api_key = "91e12b0daa1e4de9b5a5a15b4bd40a81"

# List of available news sources (excluding removed.com)
news_sources = [
    source for source in [
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
    for article in articles[:5]:  # Display only the first 5 articles
        st.write(f"**{article['source']['name']}", f", \"{article['title']}\"")
        st.write(f"**Date:** {datetime.fromisoformat(article['publishedAt']).strftime('%Y-%m-%d')}")
        st.write(f"**Link:** {article['url']}")
        st.write(f"**Synopsis:** {article['description']}")
        st.write("---")

def main():
    st.title("News Article Finder")

    # User input for search query
    query = st.text_input("Enter your research topic:")

    # Source selection
    selected_sources = st.multiselect("Select news sources:", news_sources)

    # Sort by option
    sort_by_options = ["publishedAt", "popularity", "None"]
    sort_by = st.selectbox("Sort by:", sort_by_options) 

    if st.button("Search"):
        if not query:
            st.warning("Please enter a search query.")
        else:
            try:
                articles = get_news_articles(query, selected_sources, sort_by if sort_by != "None" else None)
                display_articles(articles)
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching articles: {e}")

if __name__ == "__main__":
    main()
