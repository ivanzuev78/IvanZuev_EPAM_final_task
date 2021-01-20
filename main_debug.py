import os
from unittest.mock import MagicMock

from Data.read_zip import read_csv_from_zip
from Data.save_data_funcs import load_all_hotels, save_all_hotels
from Data.sort_hotels_data import (
    choose_biggest_cities,
    sort_hotels_by_countries_and_cities,
)

from Weather.graph_funcs import create_graph_with_min_and_max_temp
from Weather.weather_forecast import get_all_weather

from geo_funcs.geo_funcs import add_address_to_all_hotels, get_all_city_centers

if __name__ == "__main__":

    # Входные данные
    path_input = input("Path to hotels.zip: ")
    path_output = input("Path for output data: ")
    numb_of_threads = input("number of threads: ")
    appid = input("Введите ключ для получения погоды, если его нет:")

    if appid:
        from Weather.appid import add_appid

        add_appid(appid)

    # Переходим в директорию со входными данными
    os.chdir(path_input)

    # загружаем данные, если они сохранены
    if os.path.exists("all_hotels_data.json"):
        all_hotels, all_city_centers, biggest_cities = load_all_hotels()
    # Получаем все данные, если они не сохранены
    else:
        # Считываем и сортируем отели
        all_hotels = sort_hotels_by_countries_and_cities(read_csv_from_zip())
        # Получаем самые большие города
        biggest_cities = choose_biggest_cities(all_hotels)
        # Получаем все центры больших городов
        all_city_centers = get_all_city_centers(all_hotels, biggest_cities)

        # Мокаем add_address_to_all_hotels
        add_address_to_all_hotels = MagicMock(return_value=None)

        # Проходимся по всем большим городам
        for county, city in biggest_cities:
            # Доавляем адресс к каждому отелю в большом городе
            add_address_to_all_hotels(all_hotels[county][city])
            print("get weather:", county, city)
            # Обогощаем большие города погодой
            all_city_centers[county][city]["Weather"] = get_all_weather(
                all_city_centers[county][city]["Latitude"],
                all_city_centers[county][city]["Longitude"],
            )

        # Сохраняем данные в папке с входными данными, что бы в следующий раз использовать их для дебага
        save_all_hotels(all_hotels, all_city_centers, biggest_cities)

    # Переходим в директорию для сохранения
    os.chdir(path_output)

    # Рисуем графики по наибольшим городам
    for county, city in biggest_cities:
        create_graph_with_min_and_max_temp(
            all_city_centers[county][city]["Weather"], county, city
        )
