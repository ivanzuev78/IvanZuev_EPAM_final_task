from concurrent.futures.thread import ThreadPoolExecutor
from typing import Optional

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
    return get_address_by_position(df_series[1]["Latitude"], df_series[1]["Longitude"])


def add_address_to_all_hotels_in_big_cities(
    biggest_cities_df: pd.DataFrame, max_threads
) -> None:
    with ThreadPoolExecutor(max_workers=max_threads) as pool:
        biggest_cities_df["Address"] = pd.Series(
            pool.map(get_address, biggest_cities_df.iterrows())
        )


def get_top_city_df(big_cities_series: pd.Series, sorted_hotels_df: pd.DataFrame):
    """

    :param big_cities_df:
    :param sorted_hotels_df:
    :return:
    """
    return pd.DataFrame(
        {
            "Country": [country for country, _ in big_cities_series.items()],
            "City": [city for _, city in big_cities_series.items()],
            "Latitude": [
                get_center(
                    sorted_hotels_df.loc[
                        (sorted_hotels_df["Country"] == country)
                        & (sorted_hotels_df["City"] == city)
                    ],
                    "Latitude",
                )
                for country, city in big_cities_series.items()
            ],
            "Longitude": [
                get_center(
                    sorted_hotels_df.loc[
                        (sorted_hotels_df["Country"] == country)
                        & (sorted_hotels_df["City"] == city)
                    ],
                    "Longitude",
                )
                for country, city in big_cities_series.items()
            ],
        }
    )


def get_center(df, param):
    return (
        float(max(df[param], key=lambda x: float(x)))
        + float(min(df[param], key=lambda x: float(x)))
    ) / 2
