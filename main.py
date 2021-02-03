import argparse
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

from Post_processing.post_process import (
    get_city_and_day_with_highest_temp,
    get_city_and_day_with_highest_temp_delta,
    get_city_and_day_with_lowest_temp,
    get_city_with_highest_all_days_delta,
)

from Weather.graph_funcs import create_graph_with_min_and_max_temp
from Weather.weather_forecast import get_all_weather

from geo_funcs.geo_funcs import add_address_to_all_hotels, get_biggest_city_centers

if __name__ == "__main__":
    print("Program started")
    parser = argparse.ArgumentParser(description="Hotels address and weather handler")
    parser.add_argument("indir", type=str, help="Input dir")
    parser.add_argument("outdir", type=str, help="Output dir")
    parser.add_argument("--threads", type=int, help="Number of threads. Default: 100")
    parser.add_argument("--appid", type=str, help="Appid to get weather")
    args = parser.parse_args()

    if args.threads:
        numb_of_threads = args.threads
    else:
        numb_of_threads = 100

    # Переходим в директорию с отелями
    os.chdir(args.indir)

    if args.appid:
        from Weather.appid import add_appid

        add_appid(args.appid)
    print("read_csv_from_zip")
    # Считываем и сортируем отели
    all_hotels = sort_hotels_by_countries_and_cities(read_csv_from_zip())
    print("choose_biggest_cities")
    # Получаем самые большие города
    biggest_cities = choose_biggest_cities(all_hotels)
    print("get_biggest_city_centers")
    # Получаем все центры больших городов
    biggest_city_centers = get_biggest_city_centers(all_hotels, biggest_cities)
    # проходимся по всем большим городам
    for county, city in biggest_cities:
        print("add_address_to_all_hotels", county, city)
        # Доавляем адресс к каждому отелю в большом городе
        add_address_to_all_hotels(all_hotels[county][city], max_threads=numb_of_threads)
        # Обогощаем большие города погодой
        print("get_all_weather", county, city)
        biggest_city_centers[county][city]["Weather"] = get_all_weather(
            biggest_city_centers[county][city]["Latitude"],
            biggest_city_centers[county][city]["Longitude"],
            numb_of_threads,
        )

    # Переходим в директорию для сохранения
    os.chdir(args.outdir)
    print("post_processing")
    # Рисуем графики по наибольшим городам
    for county, city in biggest_cities:
        create_graph_with_min_and_max_temp(
            biggest_city_centers[county][city]["Weather"], county, city
        )

    # Сохраняем список отелей в формате CSV в файлах, содержащих не более 100 записей в каждом
    save_all_hotels_to_csv(all_hotels)

    # Сохраняем полученную информацию по центру в произвольном формате, удобном для последующего использования
    save_all_cities_centers(biggest_city_centers)

    post_process_data = {
        "highest_temp": get_city_and_day_with_highest_temp(
            biggest_city_centers, biggest_cities
        ),
        "lowest_temp": get_city_and_day_with_lowest_temp(
            biggest_city_centers, biggest_cities
        ),
        "highest_temp_delta": get_city_and_day_with_highest_temp_delta(
            biggest_city_centers, biggest_cities
        ),
        "all_days_delta": get_city_with_highest_all_days_delta(
            biggest_city_centers, biggest_cities
        ),
    }

    with open("post_process_data.json", "w") as file:
        json.dump(post_process_data, file, indent=4)

    print("Program finished")
