import csv
import os
from typing import Dict, List, Optional
from zipfile import ZipFile


def read_csv_from_zip() -> List[Dict]:
    """
    Unpack .zip file, read all .csv files, filter invalid data and return list of hotels.
    Hotel format: dict{'column': value}
    :return: List
    """
    myzip = ZipFile("hotels.zip", "r")
    for filename in myzip.namelist():
        myzip.extract(filename)

    read_csv = []
    all_hotels_filtred = []
    files = []
    for file in os.listdir():
        if file.endswith(".csv"):
            files.append(open(file))
            read_csv.append(csv.reader(files[-1]))

    for csv_reader in read_csv:
        first_row_in_file = True
        column_names = {}
        for hotel in csv_reader:
            if first_row_in_file:
                for column, col_name in enumerate(hotel):
                    column_names[col_name] = column
                    first_row_in_file = False
            else:
                filtered_hotel = filter_hotel(hotel, column_names)
                if filtered_hotel is not None:
                    all_hotels_filtred.append(filtered_hotel)

    for file in files:
        file.close()

    return all_hotels_filtred


def filter_hotel(hotel: List, column_names: Dict) -> Optional[Dict]:
    """
    Filter hotels data and create dict.
    Checks:
    1) All columns have values
    2) Id is integer
    3) Latitude and Longitude are float
    4) Latitude belongs to the interval [-90, 90]
    4) Longitude belongs to the interval [-180, 180]
    :param hotel: List of values from .csv file
    :param column_names: Dict {'column name in .csv file': index of hotels list}
    :return: Optional[Dict]
    """
    hotel_dict = {}
    if len(hotel) != len(column_names):
        return None
    if not all(hotel):
        return None
    try:
        hotel[column_names["Id"]] = int(float(hotel[column_names["Id"]]))
    except ValueError:
        return None
    try:
        hotel[column_names["Latitude"]] = float(hotel[column_names["Latitude"]])
        if (
            hotel[column_names["Latitude"]] > 90
            or hotel[column_names["Latitude"]] < -90
        ):
            raise ValueError
        hotel[column_names["Longitude"]] = float(hotel[column_names["Longitude"]])
        if (
            hotel[column_names["Longitude"]] > 180
            or hotel[column_names["Longitude"]] < -180
        ):
            raise ValueError
    except ValueError:
        return None

    for col in column_names:
        hotel_dict[col] = hotel[column_names[col]]

    return hotel_dict
