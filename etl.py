import requests
#import results as results
import json
import cfg
import pandas as pd
#from pendulum import DateTime as datetime_type


# import newscatcher
# from newscatcher import Newscatcher

URL = "https://api.newscatcherapi.com/v2/search"

topics = ['news', 'sport','tech', 'finance',
'politics', 'business', 'economics',' entertainment', 'travel', 'music', 'food']


payload = {
    'q': topics,
    'lang': 'en',
    'countries': 'UK',
    'from':'7 days ago',
    'page_size':'100'
}

headers = {
    'X-API-KEY': cfg.api_key
}

r = requests.get(URL, headers=headers, params=payload)
print(r.status_code)
news = r.json()
print(news)

# # Extract articles from the response
articles = news['articles']

# Convert articles to a DataFrame using json_normalize
df = pd.json_normalize(articles)

#Check if 'media' field is a list and convert it to a list with a single element if necessary
for article in articles:
    if 'media' not in article or not isinstance(article['media'], list):
        article['media'] = [article.get('media', None)]

for article in articles:
    if 'score' not in article or not isinstance(article['score'], list):
        article['score'] = [article.get('score', None)]

df_nested_list = pd.json_normalize(
    articles,
    record_path='media',
    meta=[
        'title',
        'author',
        'published_date',
        'excerpt',
        'summary',
        'score'
    ],
)

print(df)
print(df_nested_list)

# Merge the nested list DataFrame with the main DataFrame
df_merged = pd.concat([df, df_nested_list], axis=1)

# Print the resulting DataFrame
print(df_merged.head())

df_merged


