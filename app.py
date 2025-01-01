import streamlit as st
import requests
from datetime import datetime
import openai

# Replace with your actual OpenAI API key
openai.api_key = "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"

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

def generate_quiz_with_openai(synopsis):
    """Generates a quiz question and options using OpenAI."""
    prompt = f"Create a multiple-choice quiz question based on the following synopsis: '{synopsis}'. " \
             f"Include 4 answer options, one of which is the correct answer. " \
             f"Present the output as a JSON object with the following keys: " \
             f"'question', 'options', and 'correct_answer'."

    try:
        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt, 
            max_tokens=1024, 
            n=1, 
            stop=None, 
            temperature=0.7
        )
        quiz_data = eval(response.choices[0].text)  # Evaluate the JSON response
        return quiz_data['question'], quiz_data['options'], quiz_data['correct_answer']
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return None, None, None

def display_article_and_quiz(article):
    """Displays the article and presents the quiz."""
    st.write(f"**{article['source']['name']}", f", \"{article['title']}\"")
    st.write(f"**Date:** {datetime.fromisoformat(article['publishedAt']).strftime('%Y-%m-%d')}")
    st.write(f"**Link:** {article['url']}")
    st.write(f"**Synopsis:** {article['description']}")
    st.write("---")

    synopsis = article['description']
    question, options, correct_answer = generate_quiz_with_openai(synopsis)

    if question and options and correct_answer:
        st.write("**Quiz:**")
        user_answer = st.radio(question, options)

        if st.button("Submit"):
            if user_answer == correct_answer:
                st.success("Correct!")
            else:
                st.error("Incorrect.")
    else:
        st.warning("Failed to generate quiz questions.")

def main():
    st.title("News Article Finder & Quiz")

    query = st.text_input("Enter your research topic:")
    source_options = ['All'] + us_sources
    selected_sources = st.selectbox("Select news sources:", source_options)
    sort_by_options = ["publishedAt", "popularity"]
    sort_by = st.selectbox("Sort by:", sort_by_options, index=0) 

    if st.button("Search"):
        if not query:
            st.warning("Please enter a search query.")
        else:
            try:
                if selected_sources == 'All':
                    articles = get_news_articles(query, None, sort_by)
                else:
                    articles = get_news_articles(query, [selected_sources], sort_by)

                if articles:
                    random_article = random.choice(articles)
                    display_article_and_quiz(random_article)
                else:
                    st.warning("No articles found.")

            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching articles: {e}")

if __name__ == "__main__":
    main()
