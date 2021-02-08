from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, Optional

import pandas as pd
from geopy import Bing


def get_address_by_position(latitude: float, longitude: float) -> Optional[str]:
    location = Bing(
        "AjwkHHtQlWLTZW2xwqx3CM2MYHH2slk8IiDCJERgAL_3Uax_bHGOgVZe_1iaPUXH"
    ).reverse(f"{latitude}, {longitude}")
    if location is not None:
        return location.address.replace(",", ";")
    return None


def get_address(df_series: pd.Series) -> str:
    return get_address_by_position(df_series["Latitude"], df_series["Longitude"])


def add_address_to_one_hotel(df: pd.DataFrame) -> None:
    """
    Get hotel by link and add address to it.
    :param hotel:
    :return: None
    """
    df["Address"] = df.apply(get_address, axis=1)


def add_address_to_all_hotels_in_big_cities(
    dict_of_sorted_df: Dict, big_cities: pd.Series, max_threads
) -> None:
    with ThreadPoolExecutor(max_workers=max_threads) as pool:
        pool.map(
            add_address_to_one_hotel,
            (dict_of_sorted_df[country][city] for country, city in big_cities.items()),
        )


def get_biggest_city_df(big_cities_series: pd.Series, sorted_hotels_dict_of_df: Dict):
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
