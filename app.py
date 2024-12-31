import streamlit as st
import requests

def get_google_news_summaries(topic):
  """
  Fetches news articles related to the given topic from Google News 
  and returns a summary of each article.

  Args:
    topic: The research topic for which to find articles.

  Returns:
    A list of tuples, where each tuple contains:
      - Source name (extracted from the URL)
      - Article title
      - Article snippet (from Google News)
  """

  api_key = "YOUR_GOOGLE_NEWS_API_KEY" 
  url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}&sortBy=relevancy&pageSize=3"

  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    data = response.json()

    summaries = []
    for article in data['articles']:
      source_name = article['source']['name']
      title = article['title']
      snippet = article['description']
      summaries.append((source_name, title, snippet))

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
      for source, title, snippet in article_summaries:
        st.write(f"{source}, \"{title}\"\n{snippet}\n")
    else:
      st.write("No articles found for this topic.")
  else:
    st.warning("Please enter a topic to summarize.")
