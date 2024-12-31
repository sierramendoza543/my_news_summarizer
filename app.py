import streamlit as st
import requests
from datetime import datetime

def get_google_news_summaries(topic, sort_by="publishedAt"):
  """
  Fetches news articles related to the given topic from Google News 
  and returns a summary of each article.

  Args:
    topic: The research topic for which to find articles.
    sort_by: The sorting criteria ("publishedAt" for most recent, 
             "popularity" for most popular).

  Returns:
    A list of dictionaries, where each dictionary contains:
      - source: Source name
      - title: Article title
      - snippet: Article snippet
      - url: Article URL
      - publishedAt: Article publication date and time
  """

  api_key = "91e12b0daa1e4de9b5a5a15b4bd40a81" 
  url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}&sortBy={sort_by}&pageSize=3"

  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    data = response.json()

    summaries = []
    for article in data['articles']:
      summaries.append({
          "source": article['source']['name'],
          "title": article['title'],
          "snippet": article['description'],
          "url": article['url'],
          "publishedAt": datetime.fromisoformat(article['publishedAt']).strftime("%Y-%m-%d %H:%M:%S") 
      })

    return summaries

  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from Google News API: {e}")
    return []

# Streamlit App
st.title("News Summarizer")
user_topic = st.text_input("Enter a research topic:")

sort_by = st.radio("Sort by:", ("Published Date", "Popularity"))
sort_by = "publishedAt" if sort_by == "Published Date" else "popularity"

if st.button("Summarize"):
  if user_topic:
    article_summaries = get_google_news_summaries(user_topic, sort_by)
    if article_summaries:
      st.subheader("Results for: " + user_topic)
      for article in article_summaries:
        st.write(f"{article['source']}, \"{article['title']}\"\n{article['snippet']}\n")
        st.write(f"Published: {article['publishedAt']}")
        st.write(f"URL: {article['url']}")
        st.write("---") 
    else:
      st.write("No articles found for this topic.")
  else:
    st.warning("Please enter a topic to summarize.")
