import datetime
import json
import os
from typing import Optional

if os.path.exists("openweathermap_appid.json"):
    with open("openweathermap_appid.json", "r") as file:
        all_appid_data = json.load(file)
else:
    all_appid_data = {}


def get_appid() -> Optional[str]:
    global all_appid_data

    date = str(datetime.datetime.utcnow().date())

    for appid in all_appid_data:
        if date in all_appid_data[appid]:
            if all_appid_data[appid][date] < 1000:
                all_appid_data[appid][date] += 1
                break
        else:
            all_appid_data[appid][date] = 1
            break
    else:
        return None

    if appid:
        with open("openweathermap_appid.json", "w") as file:
            json.dump(all_appid_data, file, indent=4)

    return appid


def add_appid(appid: str) -> None:
    global all_appid_data
    if os.path.exists("openweathermap_appid.json"):
        with open("openweathermap_appid.json", "r") as file:
            all_appid_data = json.load(file)

    if appid not in all_appid_data:
        all_appid_data[appid] = {}
        with open("openweathermap_appid.json", "w") as file:
            json.dump(all_appid_data, file, indent=4)


def close_appid_for_this_day(appid: str) -> None:
    with open("openweathermap_appid.json", "r") as file:
        all_appid_data = json.load(file)

    all_appid_data[appid][str(datetime.datetime.utcnow().date())] = 1000
    with open("openweathermap_appid.json", "w") as file:
        json.dump(all_appid_data, file, indent=4)


def parse_date(date: str) -> datetime.datetime:
    return datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:10]))


def clean_appid_old_date():
    global all_appid_data

    appid_to_del = []

    for key in all_appid_data:
        for date in all_appid_data[key]:
            if datetime.datetime.utcnow() - parse_date(date) > datetime.timedelta(2):
                appid_to_del.append([key, date])

    for key, date in appid_to_del:
        del all_appid_data[key][date]

    with open("openweathermap_appid.json", "w") as file:
        json.dump(all_appid_data, file, indent=4)
