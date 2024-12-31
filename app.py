import streamlit as st
import requests

def get_google_news_summaries(topic, sources=None, sort_by="publishedAt"):
  """
  Fetches news articles related to the given topic from Google News 
  and returns a summary of each article.

  Args:
    topic: The research topic for which to find articles.
    sources: A list of source IDs to filter results (optional).
    sort_by: Sorting order: "publishedAt" (default) for most recent, 
             "popularity" for most popular.

  Returns:
    A list of dictionaries, where each dictionary contains:
      - source_name: Name of the news source.
      - title: Article title.
      - snippet: Article snippet.
      - publishedAt: Article publication date.
      - url: Article URL.
  """

  api_key = "91e12b0daa1e4de9b5a5a15b4bd40a81" 
  url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}&sortBy={sort_by}&pageSize=3"
  
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
          "publishedAt": article['publishedAt'],
          "url": article['url']
      })

    return summaries

  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from Google News API: {e}")
    return []

# Get available sources from News API
def get_all_sources():
  """
  Fetches a list of available news sources from the News API.

  Returns:
    A list of source IDs.
  """
  url = f"https://newsapi.org/v2/sources?apiKey={api_key}"
  try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return [source['id'] for source in data['sources']] 
  except requests.exceptions.RequestException as e:
    print(f"Error fetching sources from News API: {e}")
    return []

# Streamlit App
st.title("News Summarizer")

user_topic = st.text_input("Enter a research topic:")

# Get all available sources
all_sources = get_all_sources()

# Allow user to select sources
selected_sources = st.multiselect("Select sources:", all_sources, default=all_sources)

# Sorting options
sort_by_options = ["publishedAt", "popularity"]
selected_sort_by = st.selectbox("Sort by:", sort_by_options, index=0)

if st.button("Summarize"):
  if user_topic:
    article_summaries = get_google_news_summaries(user_topic, selected_sources, selected_sort_by)
    if article_summaries:
      st.subheader("Results for: " + user_topic)
      for summary in article_summaries:
        st.write(f"{summary['source_name']}, \"{summary['title']}\"\n{summary['snippet']}\nPublished: {summary['publishedAt']}\nURL: {summary['url']}")
    else:
      st.write("No articles found for this topic.")
  else:
    st.warning("Please enter a topic to summarize.")
