import os
import tweepy
import pandas as pd
from dotenv import load_dotenv

try:
    load_dotenv()
    consumer_key = os.environ["C_KEY"]
    consumer_secret = os.environ["S_C_KEY"]
    api_key_bearer = os.environ["BEARER_TOKEN"]
except KeyError:
    raise Exception("Environ vars not set. Add your keys to \".env\".")
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)
results = api.search_tweets(q='crypto', count=20)

json_data = [r._json for r in results]

df = pd.json_normalize(json_data)

# test extraction to csv
# df.to_csv("extract_test.csv")
