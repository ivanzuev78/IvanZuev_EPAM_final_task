from typing import List, Tuple


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
