import csv
import os
from zipfile import ZipFile


def read_csv_from_zip(path: str):

    # Потом подставить сюда путь из ввода пользователя, предварительно обработав.
    # os.chdir(path)
    myzip = ZipFile("hotels.zip", "r")
    for filename in myzip.namelist():
        myzip.extract(filename)

    read_csv = []
    all_hotels_filtred = []
    files = {}
    for file in os.listdir():
        if file.endswith(".csv"):
            files[file] = open(file)
            read_csv.append(csv.reader(files[file]))

    for csv_reader in read_csv:
        for hotel in csv_reader:
            filtered_hotel = filter_hotel(hotel)
            if filtered_hotel:
                all_hotels_filtred.append(filtered_hotel)

    return all_hotels_filtred


def filter_hotel(hotel: list):
    if len(hotel) != 6:
        return None
    if not all(hotel):
        return None
    try:
        hotel[0] = int(float(hotel[0]))
    except ValueError:
        return None
    try:
        hotel[4] = float(hotel[4])
        if hotel[4] > 90 or hotel[4] < -90:
            raise ValueError
        hotel[5] = float(hotel[5])
        if hotel[4] > 180 or hotel[5] < -180:
            raise ValueError
    except ValueError:
        return None
    return hotel
