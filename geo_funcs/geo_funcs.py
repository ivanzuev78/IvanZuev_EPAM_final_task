from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, List

import pandas as pd
from geopy import Nominatim


def get_city_center(hotels: List[Dict]) -> Dict:
    """
    Get list of hotels and return city center: Tuple[Latitude, Longitude]
    :param hotels:
    :return:
    """
    min_latitude = None
    max_latitude = None
    min_longitude = None
    max_longitude = None

    for hotel in hotels:
        if min_latitude is None:
            min_latitude = hotel["Latitude"]
            max_latitude = hotel["Latitude"]
            min_longitude = hotel["Longitude"]
            max_longitude = hotel["Longitude"]
        else:
            if hotel["Latitude"] < min_latitude:
                min_latitude = hotel["Latitude"]
            elif hotel["Latitude"] > max_latitude:
                max_latitude = hotel["Latitude"]
            if hotel["Longitude"] < min_longitude:
                min_longitude = hotel["Longitude"]
            elif hotel["Longitude"] > max_longitude:
                max_longitude = hotel["Longitude"]

    return {
        "Latitude": (min_latitude + max_latitude) / 2,
        "Longitude": (min_longitude + max_longitude) / 2,
    }


def get_address_by_position(latitude: float, longitude: float) -> str:
    location = Nominatim(user_agent="ivan78").reverse(f"{latitude}, {longitude}")
    if location is not None:
        return location.address.replace(",", ";")
    return "The address is not found!"


def add_address_to_one_hotel(hotel: Dict) -> None:
    """
    Get hotel by link and add address to it.
    :param hotel:
    :return: None
    """
    hotel["Address"] = get_address_by_position(hotel["Latitude"], hotel["Latitude"])


def add_address_to_all_hotels(hotels: List[Dict], max_threads=4) -> None:
    with ThreadPoolExecutor(max_workers=max_threads) as pool:
        pool.map(add_address_to_one_hotel, hotels)


def get_biggest_city_centers(
    big_cities_series: pd.Series, sorted_hotels_dict_of_df: Dict
):
    """

    :param big_cities_df:
    :param sorted_hotels_dict_of_df:
    :return:
    """
    return pd.DataFrame(
        {
            "Country": [country for country, _ in big_cities_series.items()],
            "City": [city for _, city in big_cities_series.items()],
            "Latitude": [
                get_middle(sorted_hotels_dict_of_df[country][city], "Latitude")
                for country, city in big_cities_series.items()
            ],
            "Longitude": [
                get_middle(sorted_hotels_dict_of_df[country][city], "Longitude")
                for country, city in big_cities_series.items()
            ],
        }
    )


def get_middle(df, param):
    return (
        float(max(df[param], key=lambda x: float(x)))
        + float(min(df[param], key=lambda x: float(x)))
    ) / 2
