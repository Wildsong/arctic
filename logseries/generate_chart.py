#!/usr/bin/env -S conda run -n covid python
#
#   Creates an HTML file containing the "daily cases" chart.
#
#   You should be able to generate a new chart any old time
#   by running this from the command line. 
#
#   Just do the following from a command prompt
# 
#      ./generate_chart.py my_chart.html
#
#   Then copy my_chart.html to the right place,
#
#      cp my_chart.html ~/docker/capacity/html/cases/index.html
#
import os, sys
import pandas as pd
import numpy as np
from arcgis.gis import GIS
from arcgis.features import FeatureLayer, FeatureSet, Feature, Table
from datetime import datetime
import read_cases
import plotly.graph_objects as go
from config import Config

def generate_chart(cases_df):
    # https://github.com/d3/d3-3.x-api-reference/blob/master/Formatting.md#d3_format
    cases = go.Bar(x=cases_df['date'], y=cases_df['cases'], name="Cases/day", 
        marker_color="#f09665", hoverinfo="all")
    avg   = go.Scatter(x=cases_df['date'], y=cases_df['avg'], name="7 day avg", marker_color="#671d85")
    fig = go.Figure(data=[cases,avg])
    fig.update_xaxes(dtick="M1", tickformat="%b")
    fig.update_traces(hovertemplate="%{x|%b %d}: <b>%{y} cases</b>", selector=dict(type='bar'))
    fig.update_traces(hovertemplate="%{x|%b %d}: %{y:.1f} avg", selector=dict(type='scatter'))

    timestamp = datetime.now().strftime("<i>updated %b %d %H:%M</i>")
    fig.update_layout(title="<b>Clatsop County Daily Coronavirus Cases</b><br /> %s" % timestamp)

    return fig

def update_database(current, last):
    """ 
Update the big database from the little one if the little one has new data for the big one.

current = todays data
last = the last row from the big database

Returns True if the database was updated
    """

    # If these all match then the latest data
    # has already been written to the database

    if ((last.new_cases == current.new_cases) \
        and (last.total_cases == current.total_cases) 
        and (last.last_update == current.date)):
        print("Database is current.")

        # If you want to test the update, comment this out
        # and then go in and manually delete the extra row(s).
        return False

    print("Appending the new record.")

    #return False

    attributes = {
        "utc_date": datetime.utcnow(),
        "last_update": current.date,
        "editor": os.environ.get('USERNAME') or os.environ.get('USER'),
        "source": "CC",
        "new_cases" : current.new_cases,
        "total_cases" : current.total_cases,
        "new_deaths" : current.new_deaths,
        "total_deaths" : current.total_deaths,
        "name": "Clatsop"
    }

    gis = GIS(Config.PORTAL_URL, Config.PORTAL_USER, Config.PORTAL_PASSWORD)
    layer = FeatureLayer(Config.COVID_CASES_URL, gis)
    f = Feature.from_dict({"attributes": attributes})
    fs = FeatureSet(features=[f])
    results = layer.edit_features(adds=fs)

    return True

if __name__ == '__main__':

    #date_field = 'last_update'
    #utc = False

    date_field = 'utc_date'
    utc = True

    local_sdf = read_cases.read_local_cases_df()

    current = read_cases.read_current_cases_df().iloc[0]
    print("Current data")
    print(current)

    last = local_sdf.sort_values(date_field, ascending=False).iloc[0]
    if update_database(current, last):
        # Update happened so read the data again
        local_sdf = read_cases.read_local_cases_df()

    days = 4*30
    (daily_df, total_df) = read_cases.crunch_data(local_sdf, date_field, days, utc=utc)
    fig = generate_chart(daily_df)
   
    try:
        fig.write_html(sys.argv[1])
    except IndexError:
        print("WARNING, you must give me a filename if you want HTML output.")
        fig.show()
