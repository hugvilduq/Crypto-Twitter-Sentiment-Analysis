from sqlalchemy import create_engine
import pandas as pd
import re

# Connection to database
en = create_engine('mysql+mysqlconnector://duinmat:$Mo/qdGSnX$MEi@oege.ie.hva.nl/zduinmat') 
dbConnection = en.connect() 

df = pd.read_sql("select * from Tweets_unedited_with_vaderSentiment", dbConnection) 
df.head()


df=df.drop(columns=["level_0"])
# -----------------------------------
# Cleaning
# -----------------------------------


# Remove URLs
df['content'] = df['content'].str.replace('http\S+', '',regex=True)

# Remove emojis and non-ascii characters
df=df.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))

# Remove punctuation
df['content'] = df['content'].str.replace('[^\w\s]',' ',regex=True)

# Remove line jumps
df['content'] = df['content'].str.replace('\n', ' ', regex=True)

# Remove numbers
df['content'] = df['content'].str.replace('\d+', '', regex=True)

# Remove in-between excess spaces
df['content'] = df['content'].str.replace(' +',' ',regex=True)

# Remove trailing and dragging spaces
df['content'] = df['content'].str.strip()

# Turn everything into lowercase
df['content'] = df['content'].str.lower()



# Stopwords won't be removed in this file, they could affect 
# dramatically positively or negatively the performance of the model

# -----------------------------------

# Uploading to database
df.to_sql("Tweets_clean_with_Sentiment",con = en,if_exists='replace',chunksize=10000)
