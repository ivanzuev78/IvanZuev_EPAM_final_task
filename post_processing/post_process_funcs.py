import datetime
from typing import Tuple

import pandas as pd


# noinspection PyTypeChecker
def get_city_day_max_temp(df: pd.DataFrame) -> Tuple:
    data = max(
        df.apply(
            lambda row: (
                row["Country"],
                row["City"],
                max(row["Weather"]["max"].items(), key=lambda x: x[1]),
            ),
            axis=1,
        ),
        key=lambda x: x[2][1],
    )
    return (
        data[0],
        data[1],
        str(datetime.datetime.fromtimestamp(data[2][0]).date()),
        data[2][1],
    )


# noinspection PyTypeChecker
def get_city_day_min_temp(df: pd.DataFrame) -> Tuple:

    data = min(
        df.apply(
            lambda row: (
                row["Country"],
                row["City"],
                min(row["Weather"]["min"].items(), key=lambda x: x[1]),
            ),
            axis=1,
        ),
        key=lambda x: x[2][1],
    )
    return (
        data[0],
        data[1],
        str(datetime.datetime.fromtimestamp(data[2][0]).date()),
        data[2][1],
    )


# noinspection PyTypeChecker
def get_city_day_max_temp_delta_one_day(df: pd.DataFrame) -> Tuple:
    data = max(
        df.apply(
            lambda row: (
                row["Country"],
                row["City"],
                max(
                    map(
                        lambda day_row: (
                            str(datetime.datetime.fromtimestamp(day_row[0]).date()),
                            day_row[1]["max"] - day_row[1]["min"],
                        ),
                        row["Weather"].iterrows(),
                    )
                ),
            ),
            axis=1,
        ),
        key=lambda x: x[2],
    )
    return *data[:2], *data[2]


# noinspection PyTypeChecker
def get_city_day_max_temp_delta_all_days(df: pd.DataFrame) -> Tuple:
    return max(
        df.apply(
            lambda row: (
                row["Country"],
                row["City"],
                max(row["Weather"]["max"].items(), key=lambda x: x[1])[1]
                - min(row["Weather"]["min"].items(), key=lambda x: x[1])[1],
            ),
            axis=1,
        ),
        key=lambda x: x[2],
    )
