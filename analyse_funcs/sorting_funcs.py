from typing import Dict

import pandas as pd


def sort_hotels_by_countries_and_cities(df: pd.DataFrame) -> Dict:
    return {
        country: {city: df_city for city, df_city in df_country.groupby(["City"])}
        for country, df_country in df.groupby(["Country"])
    }


def get_biggest_cities(dicts_of_df: Dict) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Country": list(dicts_of_df.keys()),
            "City": [
                max(
                    dicts_of_df[country],
                    key=lambda city: len(dicts_of_df[country][city]),
                )
                for country in dicts_of_df.keys()
            ],
        }
    )
