import json
import os

from Data.read_zip import read_csv_from_zip
from Data.save_data_funcs import (
    save_all_cities_centers,
    save_all_hotels_to_csv,
)
from Data.sort_hotels_data import (
    choose_biggest_cities,
    sort_hotels_by_countries_and_cities,
)

from Weather.graph_funcs import create_graph_with_min_and_max_temp
from Weather.weather_forecast import get_all_weather

from geo_funcs.geo_funcs import add_address_to_all_hotels, get_all_city_centers

from post_process import (
    get_city_and_day_with_highest_temp,
    get_city_and_day_with_highest_temp_delta,
    get_city_and_day_with_lowest_temp,
    get_city_with_highest_all_days_delta,
)

if __name__ == "__main__":

    # Входные данные
    path_input = input("Path to hotels.zip: ")
    path_output = input("Path for output data: ")
    numb_of_threads = input("number of threads: ")
    appid = input("Введите ключ для получения погоды, если его нет:")
    try:
        numb_of_threads = int(numb_of_threads)
    except ValueError:
        numb_of_threads = 4

    os.chdir(path_input)
    if appid:
        from Weather.appid import add_appid

        add_appid(appid)

    # Переходим в директорию с отелями

    # Считываем и сортируем отели
    all_hotels = sort_hotels_by_countries_and_cities(read_csv_from_zip())

    # Получаем самые большие города
    biggest_cities = choose_biggest_cities(all_hotels)

    # Получаем все центры больших городов
    all_city_centers = get_all_city_centers(all_hotels, biggest_cities)

    # проходимся по всем большим городам
    for county, city in biggest_cities:
        # Доавляем адресс к каждому отелю в большом городе
        add_address_to_all_hotels(all_hotels[county][city])
        # Обогощаем большие города погодой
        all_city_centers[county][city]["Weather"] = get_all_weather(
            all_city_centers[county][city]["Latitude"],
            all_city_centers[county][city]["Longitude"],
            numb_of_threads,
        )

    # Переходим в директорию для сохранения
    os.chdir(path_output)

    # Рисуем графики по наибольшим городам
    for county, city in biggest_cities:
        create_graph_with_min_and_max_temp(
            all_city_centers[county][city]["Weather"], county, city
        )

    # Сохраняем список отелей в формате CSV в файлах, содержащих не более 100 записей в каждом
    save_all_hotels_to_csv(all_hotels)

    # Сохраняем полученную информацию по центру в произвольном формате, удобном для последующего использования
    save_all_cities_centers(all_city_centers)

    post_process_data = {
        "highest_temp": get_city_and_day_with_highest_temp(
            all_city_centers, biggest_cities
        ),
        "lowest_temp": get_city_and_day_with_lowest_temp(
            all_city_centers, biggest_cities
        ),
        "highest_temp_delta": get_city_and_day_with_highest_temp_delta(
            all_city_centers, biggest_cities
        ),
        "all_days_delta": get_city_with_highest_all_days_delta(
            all_city_centers, biggest_cities
        ),
    }

    with open("post_process_data.json", "w") as file:
        json.dump(post_process_data, file, indent=4)
