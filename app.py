import streamlit as st
import requests
from datetime import datetime

# Google News API Key (Replace with your actual key)
api_key = "91e12b0daa1e4de9b5a5a15b4bd40a81"

# List of available news sources
news_sources = [
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
]

def get_news_articles(query, sources, sort_by="publishedAt"):
    """Fetches news articles from the Google News API."""
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sources": ",".join(sources),
        "sortBy": sort_by,
        "apiKey": api_key
    }

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
    sort_by = st.selectbox("Sort by:", ["publishedAt", "popularity"])

    if st.button("Search"):
        if not query:
            st.warning("Please enter a search query.")
        else:
            try:
                articles = get_news_articles(query, selected_sources, sort_by)
                display_articles(articles)
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching articles: {e}")

if __name__ == "__main__":
    main()
