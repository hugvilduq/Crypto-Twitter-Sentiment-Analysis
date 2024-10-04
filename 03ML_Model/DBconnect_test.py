from sqlalchemy import create_engine
import pandas as pd
import mysql

engine = create_engine('mysql+mysqlconnector://duinmat:$Mo/qdGSnX$MEi@oege.ie.hva.nl:3306/zduinmat')
connection = engine.raw_connection()

df = pd.read_sql("select * from Tweets_unedited", connection) 

df = pd.read_sql("SELECT * FROM hotel_reviews", con=engine)

conn = engine.raw_connection()
cur = conn.cursor()

# Some data insights at first glance. The fetching must be parametrized. 
cur.callproc('get_all_reviews')
for row in cur.stored_results():
    results=row.fetchall()
    colNamesList=row.description
colNamesList=[i[0] for i in colNamesList]

df_raw=pd.DataFrame(results, columns=colNamesList)
df_raw.head()