from collections import namedtuple

import pandas as pd

DATA_FILE = "https://bites-data.s3.us-east-2.amazonaws.com/weather-ann-arbor.csv"
STATION = namedtuple("Station", "ID Date Value")


def high_low_record_breakers_for_2015():
    """Extract the high and low record breaking temperatures for 2015

    The expected value will be a tuple with the highest and lowest record
    breaking temperatures for 2015 as compared to the temperature data
    provided.

    NOTE:
    The date values should not have any timestamps, should be a
    datetime.date() object. The temperatures in the dataset are in tenths
    of degrees Celsius, so you must divide them by 10

    Possible way to tackle this challenge:

    1. Create a DataFrame from the DATA_FILE dataset.

    2. Manipulate the data to extract the following:
       * Extract highest temperatures for each day / station pair between 2005-2015
       * Extract lowest temperatures for each  day / station  between 2005-2015
       * Remove February 29th from the dataset to work with only 365 days

    3. Separate data into two separate DataFrames:
       * high/low temperatures between 2005-2014
       * high/low temperatures for 2015

    4. Iterate over the 2005-2014 data and compare to the 2015 data:
       * For any temperature that is higher/lower in 2015 extract ID,
         Date, Value

    5. From the record breakers in 2015, extract the high/low of all the
       temperatures
       * Return those as STATION namedtuples, (high_2015, low_2015)
    """

    df = pd.read_csv(DATA_FILE, parse_dates=[1])
    df["day"] = df.Date.apply(lambda x: f"{x.month}-{x.day}")
    df["year"] = df.Date.apply(lambda x: x.year)
    df = df[df.day != "2-29"]

    df_prev = (
        df[df.year < 2015]
        .groupby(["ID", "day"])
        .Data_Value.agg(["min", "max"])
        .sort_values(["ID", "day"])
    )

    df_curr = (
        df[df.year == 2015]
        .groupby(["ID", "day"])
        .Data_Value.agg(["min", "max"])
        .sort_values(["ID", "day"])
    )

    df_all = df_prev.merge(
        df_curr, on=["ID", "day"], suffixes=["_prev", "_curr"], how="right"
    )

    highs = df_all[(df_all.max_curr > df_all.max_prev) | (df_all.max_prev == None)]
    lows = df_all[(df_all.min_curr < df_all.min_prev) | (df_all.min_prev == None)]

    highest = (
        df.set_index(["ID", "day"])
        .loc[highs.index]
        .query("year == 2015")
        .sort_values("Data_Value", ascending=False)
    ).iloc[0]

    lowest = (
        df.set_index(["ID", "day"]).loc[lows.index].sort_values("Data_Value")
    ).iloc[0]

    return (
        STATION(highest.name[0], highest.Date.date(), highest.Data_Value / 10),
        STATION(lowest.name[0], lowest.Date.date(), lowest.Data_Value / 10),
    )
