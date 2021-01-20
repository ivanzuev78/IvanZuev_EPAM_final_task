from typing import Dict, List

from Weather.weather_forecast import get_min_and_max_temp_per_day


def get_city_and_day_with_highest_temp(all_city_centers: Dict, biggest_cities: List):
    max_temp = None
    day = None
    current_city = None
    for country, city in biggest_cities:
        current_weather = max(
            get_min_and_max_temp_per_day(all_city_centers[country][city]["Weather"]),
            key=lambda x: x["max"],
        )
        if max_temp is not None:
            if current_weather["max"] > max_temp:
                max_temp = current_weather["max"]
                day = current_weather["date"]
                current_city = city
        else:
            max_temp = current_weather["max"]
            day = current_weather["date"]
            current_city = city
    return current_city, day, max_temp
