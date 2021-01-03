from typing import List, Optional, Tuple

from geopy import Nominatim


def get_city_center(
    hotels: List[List], latitude_col=4, longitude_col=5
) -> Tuple[float, float]:
    min_latitude = None
    max_latitude = None
    min_longitude = None
    max_longitude = None

    for hotel in hotels:
        if min_latitude is None:
            min_latitude = hotel[latitude_col]
            max_latitude = hotel[latitude_col]
            min_longitude = hotel[longitude_col]
            max_longitude = hotel[longitude_col]
        else:
            if hotel[latitude_col] < min_latitude:
                min_latitude = hotel[latitude_col]
            elif hotel[latitude_col] > max_latitude:
                max_latitude = hotel[latitude_col]
            if hotel[longitude_col] < min_longitude:
                min_longitude = hotel[longitude_col]
            elif hotel[longitude_col] > max_longitude:
                max_longitude = hotel[longitude_col]

    return (min_latitude + max_latitude) / 2, (min_longitude + max_longitude) / 2


def get_address_by_position(position: Tuple[float, float]) -> Optional[str]:
    location = Nominatim(user_agent="ivan78").reverse(f"{position[0]}, {position[1]}")
    if location is not None:
        return location.address.replace(",", ";")
    return None


def add_address_to_hotels(hotels: List[List]):
    for hotel in hotels:
        hotel.append(get_address_by_position((hotel[4], hotel[5])))
    return hotels


# hotels = [
#     ["1", "min_latitude", "US", "City", 0, 12.2345],
#     ["2", "max_latitude", "US", "City", 90, 42],
#     ["3", "min_longitude", "US", "City", 23, 0],
#     ["4", "max_longitude", "US", "City", 55, 90],
#     ["5", "Name", "US", "City", 78, 74.999],
#     ["6", "Name", "US", "City", 33, 59.001],
#     ["7", "Name", "US", "City", 89, 12],
# ]
#
# add_address_to_hotels(hotels)
# print(hotels)
