 # This script will run through the kaggle bitcoin twitter data, load it, and dump into remote database.

import pandas as pd
import sys 
# https://docs.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
# import pyodbc # install required libs for OS: https://github.com/mkleehammer/pyodbc/wiki/Install

import pymysql.cursors


try:
        # Connect to DB
    db_con = pymysql.connect(
        host='178.62.224.133',
        port=3306,
        user='david',
        password='XYByzgY3iqI583W8',
        db='raw_twitter',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Connected to DB")
except Exception as e:
    print("Could not connect to DB")
    print(e)
    sys.exit()

with db_con.cursor() as cursor:
    try:    
        # Create table
        sql = 'CREATE TABLE IF NOT EXISTS kaggle_btc_tweets (User_Name nvarchar(50), User_Location nvarchar(50), User_Description nvarchar(200), User_Created datetime, User_Followers int, User_Friends int, User_Favorites int, User_Verified boolean, Date datetime, Text nvarchar(300),hastags nvarchar(200), Source nvarchar(100), Is_Retweet Boolean )'
        cursor.execute(sql)
        db_con.commit()
        print("Table created")
    except:
        print("Error creating table")
        sys.exit()


# Pass kaggle file as argument
if len(sys.argv) < 2:
    print("Provide the path to the Kaggle csv file!")
    sys.exit()
else:
    print("Arguments: %s" % sys.argv)

# Create dataframe from csv
csv_file_path = sys.argv[1]
pd_csv = pd.read_csv(csv_file_path)
df = pd.DataFrame(pd_csv)


with db_con.cursor() as cursor:
    try:
        for row in df.itertuples():
            # Insert data into DB
            cursor.execute(
                'INSERT INTO kaggle_btc_tweets (User_Name, User_Location, User_Description, User_Created, User_Followers, User_Friends, User_Favorites, User_Verified, Date, Text, hastags, Source, Is_Retweet) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(
                row.user_name, row.user_location, row.user_description, row.user_created, row.user_followers, row.user_friends, row.user_favourites, row.user_verified, row.date, row.text, row.hashtags, row.source, row.is_retweet)
            )    
        cursor.commit()
        print("Successfully inserted %s rows into the database" % len(df))
    except Exception as e:
        print("Error inserting data into database")
        print(e)
        sys.exit()    


print(df)