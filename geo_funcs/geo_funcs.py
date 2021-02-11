from concurrent.futures.thread import ThreadPoolExecutor
from typing import Optional

import pandas as pd
from geopy import Bing


def get_address_by_position(df_series: pd.Series) -> Optional[str]:
    """
    Get address by latitude and longitude
    """
    latitude = df_series[1]["Latitude"]
    longitude = df_series[1]["Longitude"]
    location = Bing(
        "AjwkHHtQlWLTZW2xwqx3CM2MYHH2slk8IiDCJERgAL_3Uax_bHGOgVZe_1iaPUXH"
    ).reverse(f"{latitude}, {longitude}")
    if location is not None:
        return location.address.replace(",", ";")
    return None


def add_address_to_hotels_in_top_cities(
    top_cities_df: pd.DataFrame, max_threads
) -> None:
    """
    add address to all hotels in top cities using side effect
    """
    with ThreadPoolExecutor(max_workers=max_threads) as pool:
        top_cities_df["Address"] = pd.Series(
            pool.map(get_address_by_position, top_cities_df.iterrows())
        )


def get_top_city_df(top_cities_series: pd.Series, sorted_hotels_df: pd.DataFrame):
    """
    Analise all hotels in top cities and return dataframe with cities and its latitude, longitude
    """
    return pd.DataFrame(
        {
            "Country": [country for country, _ in top_cities_series.items()],
            "City": [city for _, city in top_cities_series.items()],
            "Latitude": [
                get_center(
                    sorted_hotels_df.loc[
                        (sorted_hotels_df["Country"] == country)
                        & (sorted_hotels_df["City"] == city)
                    ],
                    "Latitude",
                )
                for country, city in top_cities_series.items()
            ],
            "Longitude": [
                get_center(
                    sorted_hotels_df.loc[
                        (sorted_hotels_df["Country"] == country)
                        & (sorted_hotels_df["City"] == city)
                    ],
                    "Longitude",
                )
                for country, city in top_cities_series.items()
            ],
        }
    )


def get_center(df, param):
    """
    Get center latitude or longitude using data in dataframe
    """
    return (
        float(max(df[param], key=lambda x: float(x)))
        + float(min(df[param], key=lambda x: float(x)))
    ) / 2
