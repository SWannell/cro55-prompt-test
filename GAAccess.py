# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 16:32:22 2020

@author: SWannell
"""

import pandas as pd
import requests
import urllib


def get_data(gaid, start, end, metrics, dims, token, segment,
             filters="", max_results=10000):
    """Create generator to yield GA API data in chunks of size max_results"""
    # build uri w/ params
    api_uri = "https://www.googleapis.com/analytics/v3/data/ga?ids={gaid}" \
              "&start-date={start}&end-date={end}&metrics={metrics}&" \
              "dimensions={dimensions}&segment={segment}&" \
              "samplingLevel=HIGHER_PRECISION&access_token={token}&"\
              "max-results={max_results}"
    # insert uri params
    api_uri = api_uri.format(
        gaid=gaid,
        start=start,
        end=end,
        metrics=",".join(metrics),
        dimensions=",".join(dims),
        segment=segment,
        token=token,
        max_results=max_results
        )
    if len(filters) > 0:
        filter_string = "&filters=" + urllib.parse.quote_plus(filters)
        api_uri += filter_string
    # Use yield to make a generator bcs memory efficient as data DLed in chunks
    r = requests.get(api_uri)
    data = r.json()
    yield data
    if data.get("nextLink", None):
        while data.get("nextLink"):
            new_uri = data.get("nextLink")
            new_uri += "&access_token={token}".format(token=token)
            r = requests.get(new_uri)
            data = r.json()
            yield data


def to_df(gadata):
    """Takes in a generator from GAData() creates a dataframe from the rows"""
    df = None
    for data in gadata:
        if df is None:
            df = pd.DataFrame(
                    data['rows'],
                    columns=[x['name'] for x in data['columnHeaders']]
                    )
        else:
            newdf = pd.DataFrame(
                    data['rows'],
                    columns=[x['name'] for x in data['columnHeaders']]
                    )
            df = df.append(newdf)
        print("Gathered {} rows".format(len(df)))
    return df