# 
#  Load the log files into data frames and visualize them
#
import pandas as pd
import json
import matplotlib.pyplot as plot
from esri_logs import parse_log

def crunch_data(df):
    """ Return new df's. """

    df.time = pd.to_datetime(df.time, format="%Y-%m-%dT%H:%M:%S")
    df["code"] = 1

    df['hour'] = df['time'].dt.hour
    df['dayofweek'] = df['time'].dt.dayofweek
    df['dayofyear'] = df['time'].dt.dayofyear
    hourly = df.groupby('hour').count()
    day = df.groupby('dayofweek').count()
    doy = df.groupby('dayofyear').count()

    return (hourly, day, doy)


# ==================================================================================

# This is a unit test, it does no real work.

if __name__ == "__main__":

    title = "9001, 9002 SEVERE errors"

    serverlog = "logseries/sample.log"
    log = parse_log(serverlog, level=["SEVERE"], code=[9001, 9002])
    df = pd.read_json(json.dumps(log))
    (hf,df,af) = crunch_data(df)

    hf.plot(y='code', kind='bar', title=title)
    plot.show()

    df.plot(y='code', kind='bar', title=title)
    plot.show()

    af.plot(y='code', kind='bar', title=title)
    plot.show()

    print("All done.")

# That's all!
