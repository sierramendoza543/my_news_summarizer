import streamlit as st
import newsapi
from newsapi import NewsApiClient

def get_google_news_summaries(topic, sources, sort_by='relevancy'):
  """
  Fetches news articles related to the given topic from Google News 
  and returns a summary of each article.

  Args:
    topic: The research topic for which to find articles.
    sources: A list of source IDs to filter results by.
    sort_by: Sorting criteria ('relevancy' or 'publishedAt').

  Returns:
    A list of dictionaries, where each dictionary contains:
      - source_name: Name of the news source.
      - title: Article title.
      - snippet: Article snippet.
      - publishedAt: Article publication date.
      - url: Article URL.
  """

  api_key = "91e12b0daa1e4de9b5a5a15b4bd40a81" 
  newsapi = NewsApiClient(api_key=api_key)

  if sources:
    source_params = ','.join(sources)
    url = f"https://newsapi.org/v2/everything?q={topic}&sources={source_params}&sortBy={sort_by}&pageSize=3"
  else:
    url = f"https://newsapi.org/v2/everything?q={topic}&sortBy={sort_by}&pageSize=3"

  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    data = response.json()

    summaries = []
    for article in data['articles']:
      summaries.append({
          'source_name': article['source']['name'],
          'title': article['title'],
          'snippet': article['description'],
          'publishedAt': article['publishedAt'],
          'url': article['url']
      })

    return summaries

  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from Google News API: {e}")
    return []

# Get available sources from News API
newsapi = NewsApiClient(api_key="YOUR_GOOGLE_NEWS_API_KEY")
sources = newsapi.get_sources().get('sources')
source_ids = [source['id'] for source in sources]
source_options = ['All'] + [source['id'] for source in sources]

# Streamlit App
st.title("News Summarizer")

user_topic = st.text_input("Enter a research topic:")
sort_by = st.selectbox("Sort by:", ("relevancy", "publishedAt"))
selected_sources = st.multiselect("Select Sources:", source_options)

if st.button("Summarize"):
  if user_topic:
    if 'All' in selected_sources:
      selected_sources = [] 
    article_summaries = get_google_news_summaries(user_topic, selected_sources, sort_by)
    if article_summaries:
      st.subheader("Results for: " + user_topic)
      for article in article_summaries:
        st.write(f"{article['source_name']}, \"{article['title']}\"\n{article['snippet']}\nPublished: {article['publishedAt']}\nURL: {article['url']}")
    else:
      st.write("No articles found for this topic.")
  else:
    st.warning("Please enter a topic to summarize.")
