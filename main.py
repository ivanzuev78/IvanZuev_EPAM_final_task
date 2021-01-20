import os

from Data.read_zip import read_csv_from_zip
from Data.sort_hotels_data import (
    choose_biggest_cities,
    sort_hotels_by_countries_and_cities,
)

from geo_funcs.geo_funcs import add_address_to_all_hotels, get_all_city_centers

if __name__ == "__main__":

    # Входные данные
    path_input = input("Path to hotels.zip: ")
    path_output = input("Path for output data: ")
    numb_of_threads = input("number of threads: ")

    # Переходим в директорию с отелями
    os.chdir(path_input)

    # Считываем и сортируем отели
    all_hotels = sort_hotels_by_countries_and_cities(read_csv_from_zip())

    # Получаем самые большие города
    biggest_cities = choose_biggest_cities(all_hotels)

    # Получаем все центры
    all_centers = get_all_city_centers(all_hotels)

    # Доавляем адресс к каждому отелю в большом городе
    for county, city in biggest_cities:
        add_address_to_all_hotels(all_hotels[county][city])
