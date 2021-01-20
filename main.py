import os

from Data.read_zip import read_csv_from_zip
from Data.sort_hotels_data import (
    choose_biggest_cities,
    sort_hotels_by_countries_and_cities,
)

from Weather.appid import add_appid
from Weather.weather_forecast import get_all_weather

from geo_funcs.geo_funcs import add_address_to_all_hotels, get_biggest_cities_centers

if __name__ == "__main__":

    # Входные данные
    path_input = input("Path to hotels.zip: ")
    path_output = input("Path for output data: ")
    numb_of_threads = input("number of threads: ")
    appid = input("Введите ключ для получения погоды, если его нет:")

    if appid:
        add_appid(appid)

    # Переходим в директорию с отелями
    os.chdir(path_input)

    # Считываем и сортируем отели
    all_hotels = sort_hotels_by_countries_and_cities(read_csv_from_zip())

    # Получаем самые большие города
    biggest_cities = choose_biggest_cities(all_hotels)
    print(biggest_cities)
    # Получаем все центры больших городов
    biggest_centers = get_biggest_cities_centers(all_hotels, biggest_cities)
    print(biggest_centers)

    # проходимся по всем большим городам
    for county, city in biggest_cities:
        # Доавляем адресс к каждому отелю в большом городе
        add_address_to_all_hotels(all_hotels[county][city])

        # Обогощаем отели в больших городах погодой
        biggest_centers[county][city]["Weather"] = get_all_weather(
            biggest_centers[county][city]["Latitude"],
            biggest_centers[county][city]["Longitude"],
        )

    # Переходим в директорию для сохранения
    os.chdir(path_output)
