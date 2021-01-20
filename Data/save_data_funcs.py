import json
from typing import Dict


def save_all_hotels(all_hotels: Dict, all_city_centers: Dict) -> None:
    with open("all_hotels.json", "w") as file:
        json.dump(all_hotels, file)
    with open("all_city_centers.json", "w") as file:
        json.dump(all_city_centers, file)


def load_all_hotels():
    with open("all_hotels.json", "r") as file:
        all_hotels = json.load(file)
    with open("all_city_centers.json", "r") as file:
        all_city_centers = json.load(file)

    return all_hotels, all_city_centers
