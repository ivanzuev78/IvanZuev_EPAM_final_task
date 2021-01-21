import json
import os
from typing import Dict, List


def chdir_to_country_city(country: str, city: str, first_dir="") -> None:
    if first_dir:
        first_dir = os.path.join(os.getcwd(), first_dir)
        if not os.path.exists(first_dir):
            os.mkdir(first_dir)
        os.chdir(first_dir)
    else:
        first_dir = os.getcwd()
    country_path = os.path.join(first_dir, country)
    city_path = os.path.join(country_path, city)

    if not os.path.exists(country_path):
        os.mkdir(country)
    os.chdir(country_path)
    if not os.path.exists(city_path):
        os.mkdir(city_path)
    os.chdir(city_path)


def save_all_hotels(
    all_hotels: Dict, all_city_centers: Dict, biggest_cities: List
) -> None:
    all_hotels_data = {
        "all_hotels": all_hotels,
        "all_city_centers": all_city_centers,
        "biggest_cities": biggest_cities,
    }
    with open("all_hotels_data.json", "w") as file:
        json.dump(all_hotels_data, file, indent=4)


def load_all_hotels():
    with open("all_hotels_data.json", "r") as file:
        all_hotels_data = json.load(file)

    return (
        all_hotels_data["all_hotels"],
        all_hotels_data["all_city_centers"],
        all_hotels_data["biggest_cities"],
    )


def save_all_cities_centers(centers: Dict) -> None:
    with open("all_cities_centers.json", "w") as file:
        json.dump(centers, file, indent=4)


def save_all_hotels_in_one_city(
    hotels: List[Dict], country: str, city: str, file_index=1
) -> None:

    order_of_colums = list(hotels[0].keys())
    with open(f"hotels_in_{country}_{city}_{file_index}.csv", "w") as file:
        file.write("".join((f"{i}," for i in order_of_colums))[:-1] + "\n")
        for hotels_index, hotel in enumerate(hotels):
            row = ""
            for index, col in enumerate(order_of_colums):
                row += str(hotel[col])
                if index != len(order_of_colums) - 1:
                    row += ","
                else:
                    row += "\n"
            file.write(row)
            if hotels_index == 99:
                save_all_hotels_in_one_city(hotels[100:], country, city, file_index + 1)
                break


def save_all_hotels_to_csv(all_hotels: Dict, collect_in_folder="") -> None:
    """
    If we want to collect
    :param all_hotels:
    :param collect_in_one_folder:
    :return:
    """
    root_dir = os.getcwd()
    for country in all_hotels:
        for city in all_hotels[country]:
            chdir_to_country_city(country, city, collect_in_folder)
            save_all_hotels_in_one_city(all_hotels[country][city], country, city)
            os.chdir(root_dir)
