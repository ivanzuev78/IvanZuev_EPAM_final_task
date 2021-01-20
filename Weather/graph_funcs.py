import datetime
import os
import time
from typing import Dict

from Weather.weather_forecast import get_all_weather, get_min_and_max_temp_per_day

import matplotlib.pyplot as plt


def create_graph_with_min_and_max_temp(weather_data: Dict, country: str, city: str):

    current_path = os.getcwd()
    country_path = os.path.join(current_path, country)
    city_path = os.path.join(country_path, city)
    if not os.path.exists(country_path):
        os.mkdir(country)
    os.chdir(country_path)
    if not os.path.exists(city_path):
        os.mkdir(city_path)
    os.chdir(city_path)

    data = get_min_and_max_temp_per_day(weather_data)
    x = [datetime.datetime.fromtimestamp(day["date"]) for day in data]
    y_min = [day["min"] for day in data]
    y_max = [day["max"] for day in data]
    plt.plot(x, y_min)
    plt.plot(x, y_max)
    plt.xlabel("Date")
    plt.ylabel("Temperature, °C")
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.3)
    plt.grid(b=True, which="major", axis="both")
    plt.text(x[0], max(y_max) + 2, f"{country}, {city}", fontsize=14)
    plt.savefig(f"weather_{country}_{city}.jpg", pil_kwargs={"optimize": True})
    plt.clf()
    os.chdir(current_path)


if __name__ == "__main__":
    t1 = time.time()
    print(t1)
    data = get_all_weather(32.49375, -92.08275)
    t2 = time.time()
    print(t2 - t1)
    data2 = get_all_weather(45.531554, 4.278685)
    t3 = time.time()
    print(t3 - t2)
    data3 = get_all_weather(37.56611, -77.47481)
    t4 = time.time()
    print(t4 - t3)
    create_graph_with_min_and_max_temp(data, "USA", "City")
    create_graph_with_min_and_max_temp(data2, "USA", "1City")
    create_graph_with_min_and_max_temp(data3, "Rus", "22City")
    t5 = time.time()
    print("-------------")
    print(t5 - t4)
