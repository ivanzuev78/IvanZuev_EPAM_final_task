from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, List

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


def add_address_to_all_hotels(hotels: List[Dict], max_threads=100) -> None:
    with ThreadPoolExecutor(max_workers=max_threads) as pool:
        pool.map(add_address_to_one_hotel, hotels)


def get_all_city_centers(all_hotels: Dict) -> Dict:
    """
    all_centers format: {county: {city: [Latitude, Latitude]} }
    print(all_centers[country][city])
    # >>> Tuple(Latitude, Latitude)
    :param all_hotels:
    :return:
    """
    all_centers = {}
    for country in all_hotels:
        all_centers[country] = {}
        for city in all_hotels[country]:
            all_centers[country][city] = get_city_center(all_hotels[country][city])
    return all_centers
