import datetime

import matplotlib.pyplot as plt
import pandas as pd

from post_processing.dir_funcs import chdir_to_country_city


def create_graph_with_min_and_max_temp(
    weather_df: pd.DataFrame, output_folder: str, country: str, city: str
) -> None:
    with chdir_to_country_city(output_folder, country, city):
        x = [datetime.datetime.fromtimestamp(int(day)) for day in weather_df.keys()]
        y = {row.name: row.values for row in weather_df.iloc}
        plt.plot(x, y["max"], label="max temperature", color="r")
        plt.plot(x, y["min"], label="min temperature", color="b")

        plt.xlabel("Date")
        plt.ylabel("Temperature, °C")
        plt.xticks(rotation=10)
        plt.subplots_adjust(bottom=0.2)
        plt.grid(b=True, which="major", axis="both")
        plt.title(f"{country}, {city}")
        plt.legend()
        plt.savefig(f"weather_{country}_{city}.jpg", pil_kwargs={"optimize": True})
        plt.clf()


def create_all_weather_graphics(biggest_cities_df: pd.DataFrame, output_folder: str):
    """

    :param output_folder:
    :param biggest_cities_df:
    :return:
    """

    [
        create_graph_with_min_and_max_temp(
            row[1]["Weather"], output_folder, row[1]["Country"], row[1]["City"]
        )
        for row in biggest_cities_df.iterrows()
    ]
