import argparse

from analyse_funcs.sorting_funcs import (
    get_biggest_cities,
    sort_hotels_by_countries_and_cities,
)
from reading_data.read_zip import read_csv_from_zip

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Hotels address and weather handler")
    parser.add_argument("indir", type=str, help="Input dir")
    parser.add_argument("outdir", type=str, help="Output dir")
    parser.add_argument(
        "--threads", type=int, help="Number of threads. Default: 100", default=100
    )
    parser.add_argument("--appid", type=str, help="Appid to get weather")
    args = parser.parse_args()

    if args.appid:
        from weather_funcs.appid import add_appid

        add_appid(args.appid)

    # Считываем и сортируем отели
    hotels_df = read_csv_from_zip(args.indir)

    dict_of_sorted_df = sort_hotels_by_countries_and_cities(hotels_df)
    print(dict_of_sorted_df)
    # Получаем самые большие города
    dict_of_biggest_cities_df = get_biggest_cities(dict_of_sorted_df)

    # Получаем все центры больших городов

    # проходимся по всем большим городам

    # Доавляем адресс к каждому отелю в большом городе

    # Обогощаем большие города погодой

    # Рисуем графики по наибольшим городам

    # Сохраняем список отелей в формате CSV в файлах, содержащих не более 100 записей в каждом

    # Сохраняем полученную информацию по центру в произвольном формате, удобном для последующего использования
