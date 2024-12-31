import streamlit as st
import requests
from datetime import datetime

def get_google_news_summaries(topic, sort_by="relevancy", sources=None):
  """
  Fetches news articles related to the given topic from Google News 
  and returns a summary of each article, optionally sorted and filtered.

  Args:
    topic: The research topic for which to find articles.
    sort_by: Sorting criteria ("relevancy" or "publishedAt"). Defaults to "relevancy".
    sources: A list of source IDs to filter results by. Defaults to None (all sources).

  Returns:
    A list of dictionaries, where each dictionary contains:
      - source: Source name
      - title: Article title
      - snippet: Article snippet
      - publishedAt: Article publication date (formatted YYYY-MM-DD)
      - url: Article URL
  """

  api_key = "91e12b0daa1e4de9b5a5a15b4bd40a81"  # Replace with your own API key
  source_params = ','.join(sources) if sources else ''
  url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}&sortBy={sort_by}&pageSize=3&sources={source_params}"

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

    # Sort summaries based on the chosen criteria
    if sort_by == "publishedAt":
      summaries.sort(key=lambda x: datetime.fromisoformat(x['publishedAt']), reverse=True)

    return summaries

  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from Google News API: {e}")
    return []

# Get available news source options from News API
newsapi_key = "91e12b0daa1e4de9b5a5a15b4bd40a81"  # Replace with your own API key
response = requests.get(f"https://newsapi.org/v2/sources?apiKey={newsapi_key}")
response.raise_for_status()
source_data = response.json()
source_options = ['ALL'] + [source['id'] for source in source_data['sources']]  # Include 'ALL' option

# Streamlit App
st.title("News Summarizer")
user_topic = st.text_input("Enter a research topic:")

# Sorting options
sort_by_options = ["Most Recent (publishedAt)", "Most Relevant (relevancy)"]
sort_by = st.selectbox("Sort by:", sort_by_options, index=sort_by_options.index("Most Relevant (relevancy)"))
selected_sort_by = "publishedAt" if sort_by_options.index(sort_by) == 0 else "relevancy"

# Filter options (multiselect)
selected_sources = st.multiselect("Filter by Source (optional):", source_options, default=source_options[0])  # Default to 'ALL'

if st.button("Summarize"):
  if user_topic:
    article_summaries = get_google_news_summaries(user_topic, sort_by=selected_sort_by, sources=selected_sources[1:] if 'ALL' not in selected_sources else None)
    if article_summaries:
      st.subheader(f"Results for: {user_topic} (Sorted by: {sort_by})")
      for summary in article_summaries:
        st.write(f"**{summary['source']}**, \"{summary['title']}\"")
        st.write(f"Published: {summary['publishedAt']}")
        st
