import os
from zipfile import ZipFile

import pandas as pd


def read_csv_from_zip(path: str) -> pd.DataFrame:
    """
    Unpack .zip file, read all .csv files, filter invalid data and return dataframe.
    :param path: path to hotels.zip
    :return:
    """
    original_path = os.getcwd()
    os.chdir(path)

    myzip = ZipFile("hotels.zip", "r")
    read_date = []

    for filename in myzip.namelist():
        myzip.extract(filename)
        file = open(filename, encoding="utf8")
        read_date.append(filter_hotels(pd.read_csv(file)).dropna())
        file.close()

    os.chdir(original_path)
    return pd.concat(read_date, ignore_index=True)


def filter_hotels(hotels_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter hotels data and create dict.
    Checks:
    1) Latitude and Longitude are float
    2) Latitude belongs to the interval [-90, 90]
    3) Longitude belongs to the interval [-180, 180]

    :return: pd.DataFrame
    """
    indexes_to_del = []
    for index, hotel in enumerate(hotels_df.iloc):
        try:
            latitude = float(hotel["Latitude"])
            longitude = float(hotel["Longitude"])
            if latitude > 90 or latitude < -90:
                raise ValueError
            if longitude > 180 or longitude < -180:
                raise ValueError
        except ValueError:
            indexes_to_del.append(index)
            continue

    return hotels_df.drop(
        indexes_to_del,
    )
