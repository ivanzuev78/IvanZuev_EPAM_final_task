import argparse

from analyse_funcs.sorting_funcs import (
    get_biggest_cities_series,
    sort_hotels_by_countries_and_cities,
)
from geo_funcs.geo_funcs import (
    add_address_to_all_hotels_in_big_cities,
    get_biggest_city_df,
)
from reading_data.read_zip import read_csv_from_zip
from weather_funcs.weather_forecast import get_all_weather_df

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Hotels address and weather handler")
    parser.add_argument("indir", type=str, help="Input dir")
    parser.add_argument("outdir", type=str, help="Output dir")
    parser.add_argument(
        "--threads", type=int, help="Number of threads. Default: 100", default=100
    )
    parser.add_argument("--appid", type=str, help="Appid to get weather")
    args = parser.parse_args()

    # Tут будет обработка аргуметнов командной строки

    if args.appid:
        from weather_funcs.appid import add_appid

        add_appid(args.appid)

    # Считываем и сортируем отели
    hotels_df = read_csv_from_zip(args.indir)

    dict_of_sorted_df = sort_hotels_by_countries_and_cities(hotels_df)

    # Получаем самые большие города
    biggest_cities_pd_series = get_biggest_cities_series(dict_of_sorted_df)

    # Получаем все центры больших городов
    biggest_cities_df = get_biggest_city_df(biggest_cities_pd_series, dict_of_sorted_df)

    # Доавляем адресс к каждому отелю в большом городе
    add_address_to_all_hotels_in_big_cities(
        dict_of_sorted_df, biggest_cities_pd_series, max_threads=args.threads
    )

    # Обогощаем большие города погодой
    biggest_cities_df = get_all_weather_df(biggest_cities_df, max_threads=args.threads)
    # Рисуем графики по наибольшим городам

    # Сохраняем список отелей в формате CSV в файлах, содержащих не более 100 записей в каждом

    # Сохраняем полученную информацию по центру в произвольном формате, удобном для последующего использования
