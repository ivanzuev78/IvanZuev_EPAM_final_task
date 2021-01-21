import datetime
from typing import Dict, List

from Weather.weather_forecast import get_min_and_max_temp_per_day


def get_city_and_day_with_highest_temp(all_city_centers: Dict, biggest_cities: List):
    return get_city_and_day_highest_or_lowest_temp(
        all_city_centers, biggest_cities, "MAX"
    )


def get_city_and_day_with_lowest_temp(all_city_centers: Dict, biggest_cities: List):
    return get_city_and_day_highest_or_lowest_temp(
        all_city_centers, biggest_cities, "MIN"
    )


def get_city_and_day_with_highest_temp_delta(
    all_city_centers: Dict, biggest_cities: List
):
    return get_city_and_day_highest_or_lowest_temp(
        all_city_centers, biggest_cities, "DAY_DELTA"
    )


def get_city_with_highest_all_days_delta(all_city_centers: Dict, biggest_cities: List):
    return get_city_and_day_highest_or_lowest_temp(
        all_city_centers, biggest_cities, "ALL_DAYS_DELTA"
    )


def get_city_and_day_highest_or_lowest_temp(
    all_city_centers: Dict, biggest_cities: List, return_temp: str
):
    """

    :param all_city_centers:
    :param biggest_cities:
    :param return_temp: it can be 'MIN' or 'MAX' or 'DAY_DELTA' or 'ALL_DAYS_DELTA'
    :return:
    """
    max_temp = None
    max_temp_day = None
    max_temp_city = None

    min_temp = None
    min_temp_day = None
    min_temp_city = None

    day_delta = None
    day_delta_day = None
    day_delta_city = None

    all_days_delta = None
    all_days_delta_city = None

    for country, city in biggest_cities:
        weather_max = max(
            get_min_and_max_temp_per_day(all_city_centers[country][city]["Weather"]),
            key=lambda x: x["max"],
        )
        weather_min = min(
            get_min_and_max_temp_per_day(all_city_centers[country][city]["Weather"]),
            key=lambda x: x["min"],
        )
        weather_day_delta = max(
            get_min_and_max_temp_per_day(all_city_centers[country][city]["Weather"]),
            key=lambda x: x["max"] - x["min"],
        )

        current_all_days_delta = weather_max["max"] - weather_min["min"]

        if max_temp is not None:
            if weather_max["max"] > max_temp:
                max_temp = weather_max["max"]
                max_temp_day = weather_max["date"]
                max_temp_city = city
            if weather_min["min"] < min_temp:
                min_temp = weather_min["min"]
                min_temp_day = weather_min["date"]
                min_temp_city = city
            if weather_day_delta["max"] - weather_day_delta["min"] > day_delta_day:
                day_delta = weather_day_delta["max"] - weather_day_delta["min"]
                day_delta_day = weather_day_delta["date"]
                day_delta_city = city
            if current_all_days_delta > all_days_delta:
                all_days_delta = current_all_days_delta
                all_days_delta_city = city

        else:
            max_temp = weather_max["max"]
            max_temp_day = weather_max["date"]
            max_temp_city = city
            min_temp = weather_min["min"]
            min_temp_day = weather_min["date"]
            min_temp_city = city
            day_delta = weather_day_delta["max"] - weather_day_delta["min"]
            day_delta_day = weather_day_delta["date"]
            day_delta_city = city
            all_days_delta = current_all_days_delta
            all_days_delta_city = city

    if return_temp == "MAX":
        return (
            max_temp_city,
            str(datetime.datetime.fromtimestamp(max_temp_day).date()),
            max_temp,
        )
    elif return_temp == "MIN":
        return (
            min_temp_city,
            str(datetime.datetime.fromtimestamp(min_temp_day).date()),
            min_temp,
        )
    elif return_temp == "DAY_DELTA":
        return (
            day_delta_city,
            str(datetime.datetime.fromtimestamp(day_delta_day).date()),
            day_delta,
        )
    elif return_temp == "ALL_DAYS_DELTA":
        return all_days_delta_city, all_days_delta

    raise TypeError("return_temp Error")
