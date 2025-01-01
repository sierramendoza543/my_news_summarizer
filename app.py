import streamlit as st
import requests
from datetime import datetime
import random

# Google News API Key (Replace with your actual key)
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

    return data['articles']

def create_quiz(synopsis):
    """Creates a simple multiple-choice quiz based on the article synopsis."""
    # Extract keywords from the synopsis
    keywords = synopsis.split() 

    # Create a list of possible answers (including the correct answer and distractors)
    possible_answers = [
        random.choice(keywords), 
        random.choice(keywords), 
        random.choice(keywords), 
        random.choice(keywords) 
    ]
    correct_answer = random.choice(keywords) 
    possible_answers[random.randint(0, 3)] = correct_answer

    # Shuffle the answer options 
    random.shuffle(possible_answers)

    return possible_answers, correct_answer

def display_article_and_quiz(article):
    """Displays the article and presents the quiz."""
    st.write(f"**{article['source']['name']}**", f", \"{article['title']}\"")
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

    # User input for search query
    query = st.text_input("Enter your research topic:")

    # Source selection (including "All")
    source_options = ['All'] + us_sources
    selected_sources = st.selectbox("Select news sources:", source_options)

    # Sort by option with mandatory selection
    sort_by_options = ["publishedAt", "popularity"]
    sort_by = st.selectbox("Sort by:", sort_by_options, index=0)  # Default to "publishedAt"

    if st.button("Search"):
        if not query:
            st.warning("Please enter a search query.")
        else:
            try:
                if selected_sources == 'All':
                    articles = get_news_articles(query, None, sort_by)
                else:
                    articles = get_news_articles(query, [selected_sources], sort_by)

                # Select a random article
                if articles:
                    random_article = random.choice(articles)
                    display_article_and_quiz(random_article)
                else:
                    st.warning("No articles found.")

            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching articles: {e}")

if __name__ == "__main__":
    main()
