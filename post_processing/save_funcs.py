import json
import pickle
from pathlib import Path

import pandas as pd

from post_processing.post_process_funcs import (
    get_city_day_max_temp,
    get_city_day_max_temp_delta_all_days,
    get_city_day_max_temp_delta_one_day,
    get_city_day_min_temp,
)


def save_hotels_df(
    df: pd.DataFrame, big_cities_series: pd.Series, output_folder: Path
) -> None:

    for country, city in big_cities_series.items():
        df_to_save = df.loc[
            (df["Country"] == country) & (df["City"] == city)
        ].reset_index()
        path_to_file = Path(f"{output_folder}/{country}/{city}")

        for index, list_of_df_to_save in enumerate(
            df_to_save.loc[i * 100 : (i + 1) * 100 - 1]
            for i in range(int(len(df_to_save) / 100) + 1)
        ):
            list_of_df_to_save.drop("index", axis=1).to_csv(
                path_to_file / f"{country}_{city}_{index + 1}.csv", index=False
            )


def save_post_data(top_cities_df: pd.DataFrame, outdir: Path):
    """
    Save post-processing data
    """
    with open(outdir / "post_process.json", "w") as file:
        json.dump(
            {
                "city_day_max_temp": get_city_day_max_temp(top_cities_df),
                "city_day_min_temp": get_city_day_min_temp(top_cities_df),
                "city_day_max_temp_delta_one_day": get_city_day_max_temp_delta_one_day(
                    top_cities_df
                ),
                "city_day_max_temp_delta_all_days": get_city_day_max_temp_delta_all_days(
                    top_cities_df
                ),
            },
            file,
            indent=4,
        )


def save_top_cities_df(top_cities_df: pd.DataFrame, outdir: Path):
    with open(outdir / "top_cities.df", "wb") as file:
        pickle.dump(top_cities_df, file)
