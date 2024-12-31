import streamlit as st
import requests
from datetime import datetime

def get_google_news_summaries(topic):
  """
  Fetches news articles related to the given topic from Google News 
  and returns a summary of each article.

  Args:
    topic: The research topic for which to find articles.

  Returns:
    A list of dictionaries, where each dictionary contains:
      - source: Source name
      - title: Article title
      - snippet: Article snippet
      - publishedAt: Article publication date
      - url: Article URL
  """

  api_key = "91e12b0daa1e4de9b5a5a15b4bd40a81" 
  url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}&sortBy=relevancy&pageSize=3"

  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    data = response.json()

    summaries = []
    for article in data['articles']:
      source = article['source']['name']
      title = article['title']
      snippet = article['description']
      published_at = datetime.fromisoformat(article['publishedAt']).strftime('%Y-%m-%d') 
      url = article['url']
      summaries.append({
          'source': source,
          'title': title,
          'snippet': snippet,
          'publishedAt': published_at,
          'url': url
      })

    return summaries

  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from Google News API: {e}")
    return []

# Streamlit App
st.title("News Summarizer")
user_topic = st.text_input("Enter a research topic:")

if st.button("Summarize"):
  if user_topic:
    article_summaries = get_google_news_summaries(user_topic)
    if article_summaries:
      st.subheader("Results for: " + user_topic)
      for summary in article_summaries:
        st.write(f"**{summary['source']}**, \"{summary['title']}\"")
        st.write(f"Published: {summary['publishedAt']}")
        st.write(f"Snippet: {summary['snippet']}")
        st.write(f"[Read More]({summary['url']})")
        st.write("---") 
    else:
      st.write("No articles found for this topic.")
  else:
    st.warning("Please enter a topic to summarize.")
