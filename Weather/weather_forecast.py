import json
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict

from Weather.appid import get_appid

import requests


def get_current_weather_from_openweathermap(
    latitude: float, longitude: float, appid: str
) -> Dict:
    if not appid:
        raise ValueError("Invalid appid. Seems like they are over.")
    weather_response = requests.get(
        f"http://api.openweathermap.org/data/2.5/"
        f"weather?lat={latitude}&lon={longitude}&APPID={appid}"
    )
    return json.loads(weather_response.text)


def current_and_forecast_weather_data_from_openweathermap(
    latitude: float, longitude: float, appid="b84971dd925571016720b3689ae9c217"
) -> Dict:
    weather_response = requests.get(
        f"http://api.openweathermap.org/data/2.5/onecall?"
        f"lat={latitude}&lon={longitude}&APPID={appid}"
    )
    return json.loads(weather_response.text)


def historical_weather_data_from_openweathermap(
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
            return historical_weather_data_from_openweathermap(
                latitude, longitude, day, get_appid()
            )

        return wrapper

    current_time = int(time.time())
    with ThreadPoolExecutor(max_workers=100) as pool:
        all_weather_data = pool.map(
            get_one_day_hist_weather(latitude, longitude, get_appid),
            (current_time - i * 86400 for i in range(6)),
        )

    return list(all_weather_data)
