import datetime
import json
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, List

from Weather.appid import get_appid

import requests


def get_current_and_forecast_weather(
    latitude: float, longitude: float, appid: str
) -> Dict:
    weather_response = requests.get(
        f"http://api.openweathermap.org/data/2.5/onecall?"
        f"lat={latitude}&lon={longitude}&APPID={appid}&units=metric"
    )
    return json.loads(weather_response.text)


def get_one_day_historical_weather(
    latitude: float, longitude: float, day: int, appid: str
) -> Dict:
    weather_response = requests.get(
        f"http://api.openweathermap.org/data/2.5/onecall/timemachine?"
        f"lat={latitude}&lon={longitude}&dt={day}&APPID={appid}&units=metric"
    )
    return json.loads(weather_response.text)


def get_all_historical_weather(latitude: float, longitude: float):
    def get_one_day_hist_weather(latitude, longitude, get_appid):
        def wrapper(day):
            return get_one_day_historical_weather(latitude, longitude, day, get_appid())

        return wrapper

    current_time = int(time.time())
    with ThreadPoolExecutor(max_workers=100) as pool:
        all_weather_data = pool.map(
            get_one_day_hist_weather(latitude, longitude, get_appid),
            (current_time - i * 86400 for i in range(6)),
        )

    return list(all_weather_data)


def get_all_weather(latitude: float, longitude: float) -> Dict:

    current_and_forecast_weather = get_current_and_forecast_weather(
        latitude, longitude, get_appid()
    )
    return {
        "Historical": get_all_historical_weather(latitude, longitude),
        "Current": current_and_forecast_weather["current"],
        "Forecast": current_and_forecast_weather["daily"],
    }


def get_min_and_max_temp_per_day(weather: Dict) -> List[Dict]:
    weather_date = []
    for day in weather["Historical"]:
        sorted_day_by_temperature = sorted(day["hourly"], key=lambda x: x["temp"])
        weather_date.append(
            {
                "date": day["hourly"][0]["dt"],
                "min": sorted_day_by_temperature[0]["temp"],
                "max": sorted_day_by_temperature[-1]["temp"],
            }
        )
    for day in weather["Forecast"]:
        weather_date.append(
            {
                "date": day["dt"],
                "min": day["temp"]["min"],
                "max": day["temp"]["max"],
            }
        )

    return weather_date


if __name__ == "__main__":
    data = get_all_weather(40.189476, -74.92503)

    for day in get_min_and_max_temp_per_day(data):
        date = day["date"]

    data = sorted(get_min_and_max_temp_per_day(data), key=lambda x: x["date"])

    x = [datetime.datetime.fromtimestamp(day["date"]) for day in data]
    y_min = [day["min"] for day in data]
    y_max = [day["max"] for day in data]

    import matplotlib.pyplot as plt

    plt.plot(x, y_min)
    plt.plot(x, y_max)
    plt.show()

    # with open('get_all_weather_return.json', 'w') as file:
    #     json.dump(data, file, indent=4)
