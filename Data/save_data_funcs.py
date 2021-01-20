import json
from typing import Dict, List


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
