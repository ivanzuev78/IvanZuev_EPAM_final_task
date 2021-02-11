import argparse

from analyse_funcs.sorting_funcs import get_top_cities_hotels_df, get_top_cities_series
from analyse_funcs.validate_funcs import validate_input
from geo_funcs.geo_funcs import add_address_to_hotels_in_top_cities, get_top_city_df
from post_processing.save_funcs import (
    save_hotels_df,
    save_post_data,
    save_top_cities_df,
)
from reading_data.read_zip import read_csv_from_zip
from weather_funcs.graph_funcs import create_weather_graphics
from weather_funcs.weather_forecast import get_all_weather_df

if __name__ == "__main__":
    print("parse args")
    parser = argparse.ArgumentParser(description="Hotels address and weather handler")
    parser.add_argument(
        "--input_file",
        type=str,
        help="Input file with hotels",
        default="input_data/hotels.zip",
    )
    parser.add_argument(
        "--outdir", type=str, help="Output dir to save data", default="output_data"
    )
    parser.add_argument(
        "--threads", type=int, help="Number of threads. Default: 64", default=64
    )
    parser.add_argument("--appid", type=str, help="Appid to get weather")
    parser.add_argument(
        "--appidpath",
        type=str,
        help="Path to openweathermap_appid.json.",
        default="input_data/openweathermap_appid.json",
    )

    print("Handle args")
    # Обработка аргуметнов командной строки
    input_file, outdir, threads, appid = validate_input(parser.parse_args())

    print("read_csv_from_zip")
    # Считываем и сортируем отели
    hotels_df = read_csv_from_zip(input_file)

    print("get_top_cities_hotels_df")
    # Отели только больших городов
    top_cities_hotels_df = get_top_cities_hotels_df(hotels_df)

    print("get_top_cities_series")
    # Получаем самые большие города
    top_cities_series = get_top_cities_series(top_cities_hotels_df)

    print("get_top_city_df")
    # Получаем все центры больших городов
    top_cities_df = get_top_city_df(top_cities_series, top_cities_hotels_df)

    print("add_address_to_all_hotels_in_big_cities")
    # Доавляем адресс к каждому отелю в большом городе
    add_address_to_hotels_in_top_cities(
        top_cities_hotels_df, max_threads=parser.parse_args().threads
    )

    print("get_all_weather_df")
    # Обогощаем большие города погодой
    top_cities_df = get_all_weather_df(top_cities_df, threads, appid)

    print("create_all_weather_graphics")
    # Рисуем графики по наибольшим городам
    create_weather_graphics(top_cities_df, outdir)

    print("save_post_data")
    # Сохраняем данные пост-процессинга
    save_post_data(top_cities_df, outdir)

    print("save_top_cities_df")
    # Сохраняем полученную информацию по центру в произвольном формате, удобном для последующего использования
    save_top_cities_df(top_cities_df, outdir)

    print("save_hotels_df")
    # Сохраняем список отелей в формате CSV в файлах, содержащих не более 100 записей в каждом
    save_hotels_df(top_cities_hotels_df, top_cities_series, outdir)
