from typing import Dict

import pandas as pd


def sort_hotels_by_countries_and_cities(df: pd.DataFrame) -> Dict:
    return {
        country: {city: df_city for city, df_city in df_country.groupby(["City"])}
        for country, df_country in df.groupby(["Country"])
    }


def get_biggest_cities_series(dicts_of_df: Dict) -> pd.Series:
    return pd.Series(
        {
            country: city
            for country, city in zip(
                dicts_of_df.keys(),
                [
                    max(
                        dicts_of_df[count],
                        key=lambda city: len(dicts_of_df[count][city]),
                    )
                    for count in dicts_of_df.keys()
                ],
            )
        }
    )
