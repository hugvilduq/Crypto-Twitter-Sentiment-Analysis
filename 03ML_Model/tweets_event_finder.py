import datetime
import numpy as np
import pandas as pd

from sqlalchemy import create_engine


# Fetch tweets from Oege/another database
sql = """
SELECT COUNT(*) as amount_of_tweets, avg(vaderSentiment_number) as avg_sentiment, year(date) as year, month(date) as month, day(date) as day, hour(date) as hour
FROM Tweets_clean_with_Sentiment
GROUP BY year(date), month(date), day(date), hour(date)
ORDER BY year(date), month(date), day(date), hour(date);
"""
con = create_engine("mysql+mysqlconnector://duinmat:$Mo/qdGSnX$MEi@oege.ie.hva.nl/zduinmat")
dfSenti = pd.read_sql(sql, con=con)

# fetch all dates of tweets, remove the (identical) timezone and round all values down to the hour
# dfData["date"] = dfData.date.str.split(pat="+").str[0].astype("datetime64")
# dfData["date"] = dfData.date.dt.floor("H")

# fix data format in dfSenti as the avg sentiment calculation could not be performed with correct dates.
dates = pd.DataFrame({"year": dfSenti["year"], "month": dfSenti["month"], "day": dfSenti["day"],
                                "hour": dfSenti["hour"], "minute": 00, "second": 00})
dfSenti["date"] = pd.to_datetime(dates)

# get the first and last date in the data and define the delta between times to use later.
start_date = dfSenti["date"].iloc[0]
end_date = dfSenti["date"].iloc[-1]
delta = datetime.timedelta(hours=1)

# Let pandas make a list of all hour times between the first and last date value in the dataset.
uniques = pd.date_range(start_date, end_date, freq="H")  # bug here with not all dates being parced (?)

# make a new destination dataframe 
df = pd.DataFrame({"date": list(uniques), "tweetcount": 0, "static_volume_event": "none", "dynamic_volume_event": "none", "avg_sentiment": 0, "static_sentiment_event": "neu", "dynamic_sentiment_event": "neu"})

print(dfSenti.date.head(10))
print(df.date.head(10))

# _ Yoinks tweets for every hour of the day and write them down in the dataframe. (tweetcount)
for _, row in dfSenti.iterrows():
    df.loc[df["date"] == row.date, "tweetcount"] = dfSenti["amount_of_tweets"]
    df.loc[df["date"] == row.date, "avg_sentiment"] = dfSenti["avg_sentiment"]
    # print(type(date))
    # print(type(df["date"]))
    # df["tweetcount"] = np.where(df["date"] == date, dfSenti["amount_of_tweets"], df["tweetcount"])


# _ Determine if a static volume event has taken place. (static_volume_event)
# _ A high event is when the count of the tweets in that hour has exceeded the 80th percentile of the whole set.
# _ A low event is when the count of the tweets in that hour has not exceeded the 20th percentile of the whole set.
# Define the 20th and 80th percentile of all tweets per hour over the full timeframe.
topTwentyCount = np.percentile(df.tweetcount, 80)
bottomTwentyCount = np.percentile(df.tweetcount, 20)
# Change the value for static_volume_event when the condition explained above is satisfied, else leave untouched.
df["static_volume_event"] = np.where(df["tweetcount"] >= topTwentyCount, "high", df["static_volume_event"])
df["static_volume_event"] = np.where(df["tweetcount"] <= bottomTwentyCount, "low", df["static_volume_event"])


# _ Determine if a dynamic volume event has taken place. (dynamic_volume_event).
# _ This is done by comparing the volume of the previous hour to the 3 hours before the current one.
volume_shift = 1.1
v_shift_1 = df["tweetcount"].shift(-1)
v_shift_2 = df["tweetcount"].shift(-2)
v_shift_3 = df["tweetcount"].shift(-3)

df["dynamic_volume_event"] = np.where(df["tweetcount"] >= ((v_shift_1 + v_shift_2 + v_shift_3) / (3 * volume_shift))
                                      , "high", df["dynamic_volume_event"])
df["dynamic_volume_event"] = np.where(df["tweetcount"] >= ((v_shift_1 + v_shift_2 + v_shift_3) / (3 / volume_shift))
                                      , "low", df["dynamic_volume_event"])


# _ Determine if a static sentiment event has taken place (sentiment_static_event)
# _ This is when the average sentiment over a given hour is between certain boundaries.
# _ >= +0.1 = positive, +0.1 > value > -0.1 = neutral, <-0.1 = negative.
posBoundary = 0.1
negBoundary = -0.1
df["static_sentiment_event"] = np.where(df["avg_sentiment"] >= posBoundary, "pos", df["static_sentiment_event"])
df["static_sentiment_event"] = np.where(df["avg_sentiment"] >= negBoundary, "neg", df["static_sentiment_event"])

# _ Determine if a dynamic sentiment event has taken place (sentiment_dynamic_event)
# _ This is when the sentiment of the past 3 hours compared to the current hour's sentiment
# _ has shifted by more than 5%. (-5% = neg, 5% = pos, else neu)
sentiment_shift = 1.03

s_shift_1 = df["avg_sentiment"].shift(-1)
s_shift_2 = df["avg_sentiment"].shift(-2)
s_shift_3 = df["avg_sentiment"].shift(-3)
df["dynamic_sentiment_event"] = np.where(df["avg_sentiment"] >= ((s_shift_1 + s_shift_2 + s_shift_3) / (3 * sentiment_shift))
                                      , "pos", df["dynamic_sentiment_event"])
df["dynamic_sentiment_event"] = np.where(df["avg_sentiment"] >= ((s_shift_1 + s_shift_2 + s_shift_3) / (3 / sentiment_shift))
                                      , "neg", df["dynamic_sentiment_event"])

# push the event list and tweet count to sql.
df.to_sql("twitter_events", con=con, if_exists="replace", index=False)
