from typing import Dict, List, Optional, Tuple

from geopy import Nominatim


def get_city_center(hotels: List[Dict]) -> Tuple[float, float]:
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

    return (min_latitude + max_latitude) / 2, (min_longitude + max_longitude) / 2


def get_address_by_position(latitude: float, longitude: float) -> Optional[str]:
    location = Nominatim(user_agent="ivan78").reverse(f"{latitude}, {longitude}")
    if location is not None:
        return location.address.replace(",", ";")
    return None


def add_address_to_hotels(hotels: List[Dict]) -> List[Dict]:
    for hotel in hotels:
        hotel["Address"] = get_address_by_position(
            hotel["Latitude"], hotel["Longitude"]
        )
    return hotels


# column_names = {"Id": 0, "Name": 1, "Country": 2, "City": 3, "Latitude": 4, "Longitude": 5}
# hotels_list = [
#     ["1", "min_latitude", "US", "City", 0, 12.2345],
#     ["2", "max_latitude", "US", "City", 90, 42],
#     ["3", "min_longitude", "US", "City", 23, 0],
#     ["4", "max_longitude", "US", "City", 55, 90],
#     ["5", "Name", "US", "City", 78, 74.999],
#     ["6", "Name", "US", "City", 33, 59.001],
#     ["7", "Name", "US", "City", 89, 12],
# ]
# hotels = [{col: col_value for col, col_value in zip(column_names, hotel)} for hotel in hotels_list]
# add_address_to_hotels(hotels)
# print(*hotels, sep='\n')
