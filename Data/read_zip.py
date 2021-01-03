import csv
import os
from typing import Dict, List, Optional
from zipfile import ZipFile


def read_csv_from_zip(path: str):

    # Потом подставить сюда путь из ввода пользователя, предварительно обработав.
    # os.chdir(path)
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
                if filtered_hotel:
                    all_hotels_filtred.append(filtered_hotel)

    for file in files:
        file.close()

    return all_hotels_filtred


def filter_hotel(hotel: List, column_names: Dict) -> Optional[Dict]:
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
