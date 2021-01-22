import datetime
import os
from typing import Dict

from Data.save_data_funcs import chdir_to_country_city

from Weather.weather_forecast import get_min_and_max_temp_per_day

import matplotlib.pyplot as plt


def create_graph_with_min_and_max_temp(
    weather_data: Dict, country: str, city: str, collect_in_folder=""
) -> None:
    current_path = os.getcwd()
    chdir_to_country_city(country, city, collect_in_folder)

    data = get_min_and_max_temp_per_day(weather_data)
    x = [datetime.datetime.fromtimestamp(day["date"]) for day in data]
    y_min = [day["min"] for day in data]
    y_max = [day["max"] for day in data]
    plt.plot(x, y_max, label="max temperature", color="r")
    plt.plot(x, y_min, label="min temperature", color="b")
    plt.xlabel("Date")
    plt.ylabel("Temperature, °C")
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.3)
    plt.grid(b=True, which="major", axis="both")
    plt.title(f"{country}, {city}")
    plt.legend()
    plt.savefig(f"weather_{country}_{city}.jpg", pil_kwargs={"optimize": True})
    plt.clf()
    os.chdir(current_path)
