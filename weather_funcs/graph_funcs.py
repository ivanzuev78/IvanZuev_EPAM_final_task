import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def create_graph_with_min_and_max_temp(
    weather_df: pd.DataFrame, output_folder: Path, country: str, city: str
) -> None:
    """
    Create one weather graphic and save it in {output_folder}/{Country}/{City}/weather_{country}_{city}.jpg
    """
    x = [datetime.datetime.fromtimestamp(int(day)) for day in weather_df.index]
    plt.plot(x, weather_df["max"], label="max temperature", color="r")
    plt.plot(x, weather_df["min"], label="min temperature", color="b")
    plt.xlabel("Date")
    plt.ylabel("Temperature, °C")
    plt.xticks(rotation=10)
    plt.subplots_adjust(bottom=0.2)
    plt.grid(b=True, which="major", axis="both")
    plt.title(f"{country}, {city}")
    plt.legend()
    path_to_file = Path(f"{output_folder}/{country}/{city}")
    path_to_file.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        path_to_file / f"weather_{country}_{city}.jpg", pil_kwargs={"optimize": True}
    )
    plt.clf()


def create_weather_graphics(biggest_cities_df: pd.DataFrame, output_folder: Path):
    """
    Create all weather graphics and save them in {output_folder}/{Country}/{City}
    """
    for row in biggest_cities_df.iterrows():
        create_graph_with_min_and_max_temp(
            row[1]["Weather"], output_folder, row[1]["Country"], row[1]["City"]
        )
