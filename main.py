import argparse
import os
import sys
from pathlib import Path

from analyse_funcs.sorting_funcs import get_top_cities_hotels_df, get_top_cities_series
from geo_funcs.geo_funcs import add_address_to_all_hotels_in_big_cities, get_top_city_df
from post_processing.save_funcs import (
    save_hotels_df,
    save_post_data,
    save_top_cities_df,
)
from reading_data.read_zip import read_csv_from_zip
from weather_funcs.appid_class import AppId
from weather_funcs.graph_funcs import create_all_weather_graphics
from weather_funcs.weather_forecast import get_all_weather_df

if __name__ == "__main__":

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

    args = parser.parse_args()

    # Tут будет обработка аргуметнов командной строки
    if not os.path.exists(args.input_file):
        sys.exit(f"Cannot find file with hotels: invalid '{args.input_file}'")

    threads = args.threads if args.threads > 0 else 64
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    input_file = Path(args.input_file)
    path_to_appid = Path(args.appidpath)
    appid_conductor = AppId(args.appidpath)

    if args.appid:
        appid_conductor.add_appid(args.appid)

    # Считываем и сортируем отели
    hotels_df = read_csv_from_zip(input_file)

    # Отели только больших городов
    top_cities_hotels_df = get_top_cities_hotels_df(hotels_df)

    # Получаем самые большие города
    top_cities_series = get_top_cities_series(top_cities_hotels_df)

    # Получаем все центры больших городов
    top_cities_df = get_top_city_df(top_cities_series, top_cities_hotels_df)

    # Доавляем адресс к каждому отелю в большом городе
    add_address_to_all_hotels_in_big_cities(
        top_cities_hotels_df, max_threads=args.threads
    )

    # Обогощаем большие города погодой
    top_cities_df = get_all_weather_df(
        top_cities_df, threads, appid_conductor.get_appid
    )

    # Рисуем графики по наибольшим городам
    create_all_weather_graphics(top_cities_df, outdir)

    # Сохраняем данные пост-процессинга
    save_post_data(top_cities_df, outdir)

    # Сохраняем полученную информацию по центру в произвольном формате, удобном для последующего использования
    save_top_cities_df(top_cities_df, outdir)

    # Сохраняем список отелей в формате CSV в файлах, содержащих не более 100 записей в каждом
    save_hotels_df(top_cities_hotels_df, top_cities_series, outdir)
