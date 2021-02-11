import json
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Callable, Dict, List

import pandas as pd
import requests


def get_current_and_forecast_weather(
    latitude: float, longitude: float, appid: Callable
) -> Dict:
    weather_response = requests.get(
        f"http://api.openweathermap.org/data/2.5/onecall?"
        f"lat={latitude}&lon={longitude}&APPID={appid()}&units=metric"
    )
    return json.loads(weather_response.text)


def get_one_day_historical_weather(
    latitude: float, longitude: float, day: int, appid: Callable
) -> Dict:
    weather_response = requests.get(
        f"http://api.openweathermap.org/data/2.5/onecall/timemachine?"
        f"lat={latitude}&lon={longitude}&dt={day}&APPID={appid()}&units=metric"
    )
    return json.loads(weather_response.text)


def get_all_historical_weather(
    latitude: float, longitude: float, threads: int, appid: Callable
):
    def get_one_day_hist_weather(
        latitude: float, longitude: float, get_appid: Callable
    ):
        def wrapper(day):
            return get_one_day_historical_weather(latitude, longitude, day, get_appid)

        return wrapper

    current_time = int(time.time() + time.timezone)
    with ThreadPoolExecutor(max_workers=threads) as pool:
        all_weather_data = pool.map(
            get_one_day_hist_weather(latitude, longitude, appid),
            (current_time - i * 86400 for i in range(5)),
        )
    return list(all_weather_data)


def get_all_weather(
    latitude: float, longitude: float, threads: int, appid: Callable
) -> Dict:

    current_and_forecast_weather = get_current_and_forecast_weather(
        latitude, longitude, appid
    )
    return {
        "Historical": get_all_historical_weather(latitude, longitude, threads, appid),
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

    return sorted(weather_date, key=lambda x: x["date"])


def get_all_weather_df(
    biggest_cities: pd.DataFrame, max_threads: int, appid: Callable
) -> pd.DataFrame:
    with ThreadPoolExecutor(max_workers=max_threads) as pool:
        data = pool.map(
            get_weather(max_threads, appid),
            (row[1] for row in biggest_cities.iterrows()),
        )

    biggest_cities["Weather"] = pd.DataFrame({"Weather": list(data)})
    return biggest_cities


def get_weather(threads: int, appid: Callable) -> callable:
    def wrapper(df_row: pd.Series) -> pd.DataFrame:
        weather = get_min_and_max_temp_per_day(
            get_all_weather(df_row["Latitude"], df_row["Longitude"], threads, appid)
        )
        return pd.DataFrame(
            {
                "max": [day_weather["max"] for day_weather in weather],
                "min": [day_weather["min"] for day_weather in weather],
            },
            index=[day_weather["date"] for day_weather in weather],
        )

    return wrapper
