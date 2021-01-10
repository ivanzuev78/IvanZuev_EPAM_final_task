import json
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, List

from Weather.appid import get_appid

import requests


def get_current_weather_from_openweathermap(
    latitude: float, longitude: float, appid: str
) -> Dict:
    if not appid:
        raise ValueError("Invalid appid. Seems like they are over.")
    weather_response = requests.get(
        f"http://api.openweathermap.org/data/2.5/"
        f"weather?lat={latitude}&lon={longitude}&APPID={appid}&units=metric"
    )
    return json.loads(weather_response.text)


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
        sorted_day_by_temperature = sorted(day["hourly"], key=lambda x: x["dt"])
        weather_date.append(
            {
                "date": (day["hourly"][0]["dt"]),
                "min": sorted_day_by_temperature[0],
                "max": sorted_day_by_temperature[-1],
            }
        )

    pass
