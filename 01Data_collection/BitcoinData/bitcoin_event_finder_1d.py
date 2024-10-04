
import pandas as pd

from sqlalchemy import create_engine

btcCSV = "Datafiles\Bitfinex_BTCUSD_1h_v2.csv"
df = pd.read_csv(btcCSV, sep=",")

# Filter all useless columns away, could be removed if you prefer.
df = df[["unix", "close"]]
df.dropna()

# This code is necessary to make sure the lowest value is on index 0.
# If the source file already has this, then this can be commented/removed.
# If that is not the case, then this is necessary to make the loop work.
df.sort_values("unix", inplace=True)

# # This could be set to any value we want, as long as the jump is able to be made in the dataframe.
hrs = 24
timeframeEvent = hrs * 3600000

# This filter is to make sure that each time value is the same length.
# This is necessary because the csv switches between seconds and milliseconds halfway.

# This is for fixing the stupid timestamp format in the original bitfinex file.
# I'm keeping this in just in case we need to fix more of these issues.
# for index, row in df.iterrows():
#     unixVal = row.unix
#     unixLen = len(str(unixVal))
#     if unixLen == 12:
#         df.loc[index, "unix"] = unixVal * 1000

unixStart = df.unix.iloc[0]
unixCount = unixStart
unixEnd = df.unix.iloc[-1]

resultList = []

while unixCount + timeframeEvent <= unixEnd:
    btcNow = None
    btcFuture = None
    futureUnix = unixCount + timeframeEvent
    try:
        btcNow = df[df["unix"] == unixCount]["close"].iloc[0]
        btcFuture = df[df["unix"] == futureUnix]["close"].iloc[0]
    except IndexError:
        btcNow = int() if btcNow is None else btcNow
        btcFuture = int() if btcFuture is None else btcFuture
        deltaBtc = int(0)
    else:
        deltaBtc = btcFuture/btcNow
    event = 1 if deltaBtc > 1.05 or deltaBtc < 0.95 else 0
    resultList.append([unixCount, btcNow, futureUnix, btcFuture, deltaBtc, event])
    unixCount += timeframeEvent

dfResult = pd.DataFrame(resultList, columns=["unixNow", "btcNow", "unixFuture", "btcFuture", "delta", "event"])

con = create_engine("mysql+mysqlconnector://duinmat:$Mo/qdGSnX$MEi@oege.ie.hva.nl/zduinmat")
dfResult.to_sql("bitcoin_events1d", if_exists="replace", con=con, index=False)
