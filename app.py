import streamlit as st
import requests
from datetime import datetime

def get_google_news_summaries(topic, sort_by="publishedAt", order="desc", sources=[]):
  """
  Fetches news articles related to the given topic from Google News 
  and returns a summary of each article.

  Args:
    topic: The research topic for which to find articles.
    sort_by: Sorting criteria ("publishedAt" for date, "popularity" for popularity score)
    order: Sorting order ("asc" for ascending, "desc" for descending)
    sources: List of source names to filter by (optional)

  Returns:
    A list of dictionaries, where each dictionary contains:
      - source_name: Name of the news source
      - title: Article title
      - snippet: Article snippet
      - publishedAt: Publication date and time
      - url: Article URL
  """

  api_key = "91e12b0daa1e4de9b5a5a15b4bd40a81" 
  url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}&sortBy={sort_by}&order={order}&pageSize=3"

  if sources:
    url += f"&sources={','.join(sources)}" 

  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    data = response.json()

    summaries = []
    for article in data['articles']:
      summaries.append({
          "source_name": article['source']['name'],
          "title": article['title'],
          "snippet": article['description'],
          "publishedAt": datetime.fromisoformat(article['publishedAt']).strftime('%Y-%m-%d %H:%M:%S'), 
          "url": article['url']
      })

    return summaries

  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from Google News API: {e}")
    return []

# Streamlit App
st.title("News Summarizer")

user_topic = st.text_input("Enter a research topic:")

sort_by = st.selectbox("Sort by:", ("publishedAt", "popularity"))
order = st.selectbox("Order:", ("desc", "asc"))

available_sources = ["the-new-york-times", "the-wall-street-journal", "cnn", "bbc-news"]  # Example list of sources
selected_sources = st.multiselect("Select sources:", available_sources)

if st.button("Summarize"):
  if user_topic:
    article_summaries = get_google_news_summaries(user_topic, sort_by, order, selected_sources)
    if article_summaries:
      st.subheader("Results for: " + user_topic)
      for article in article_summaries:
        st.write(f"{article['source_name']}, \"{article['title']}\"\n{article['snippet']}\nPublished: {article['publishedAt']}\nURL: {article['url']}")
    else:
      st.write("No articles found for this topic.")
  else:
    st.warning("Please enter a topic to summarize.")
