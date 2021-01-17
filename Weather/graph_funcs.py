import datetime
from typing import Dict

from Weather.weather_forecast import get_all_weather, get_min_and_max_temp_per_day

import matplotlib.pyplot as plt


def create_graph_with_min_and_max_temp(weather_data: Dict, country: str, city: str):
    data = get_min_and_max_temp_per_day(weather_data)
    x = [datetime.datetime.fromtimestamp(day["date"]) for day in data]
    y_min = [day["min"] for day in data]
    y_max = [day["max"] for day in data]
    fig, ax = plt.subplots()
    plt.plot(x, y_min)
    plt.plot(x, y_max)
    plt.xlabel("Date")
    plt.ylabel("Temperature, °C")
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.3)
    plt.grid(b=True, which="major", axis="both")
    fig.savefig(f"weather_{country}_{city}.jpg", pil_kwargs={"optimize": True})


if __name__ == "__main__":
    data = get_all_weather(40.189476, -74.92503)
    create_graph_with_min_and_max_temp(data, "Country", "City")
