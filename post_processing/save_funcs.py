from pathlib import Path

import pandas as pd


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
