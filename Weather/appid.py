"""
In the file "openweathermap_appid.json" there are all appid.
Appid are needed to get request to openweathermap.com.
There are some restrictions of using free accounts (only 1000 requests per day),
so this module remember the number of requests of each appid and return working appid.
I don't want to push file with appid to GitHub, so you can ask me for it.
Or it can be created manually:

if __name__ == '__main__':
    add_appid('your_appid')


"""
import datetime
import json
import os
from typing import Optional

path_to_appid_json = os.getcwd()

if os.path.exists("openweathermap_appid.json"):
    with open("openweathermap_appid.json", "r") as file:
        all_appid_data = json.load(file)
else:
    all_appid_data = {}


def save_appid_data():
    current_path = os.getcwd()
    os.chdir(path_to_appid_json)
    with open("openweathermap_appid.json", "w") as file:
        json.dump(all_appid_data, file, indent=4)
    os.chdir(current_path)


def get_appid() -> Optional[str]:
    """
    Return actual appid.
    :return:
    """
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
        save_appid_data()

    return appid


def add_appid(appid: str) -> None:
    """
    Function to add appid to the file and use it.
    :param appid:
    :return:
    """
    global all_appid_data
    if os.path.exists("openweathermap_appid.json"):
        with open("openweathermap_appid.json", "r") as file:
            all_appid_data = json.load(file)

    if appid not in all_appid_data:
        all_appid_data[appid] = {}
        save_appid_data()


def close_appid_for_this_day(appid: str) -> None:
    """
    If there are some problems with appid, it can be closed for this day.
    :param appid: str
    :return: None
    """
    with open("openweathermap_appid.json", "r") as file:
        all_appid_data = json.load(file)

    all_appid_data[appid][str(datetime.datetime.utcnow().date())] = 1000
    save_appid_data()


def parse_date(date: str) -> datetime.datetime:
    """
    Accept data in "YYYY-MM-DD" format and return datetime.datetime object.
    :param date: str
    :return: datetime.datetime
    """
    return datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:10]))


def clean_appid_old_date():
    """
    Clean "openweathermap_appid.json" by deleting the previous dates.
    :return:
    """
    global all_appid_data

    appid_to_del = []

    for key in all_appid_data:
        for date in all_appid_data[key]:
            if datetime.datetime.utcnow() - parse_date(date) > datetime.timedelta(2):
                appid_to_del.append([key, date])

    for key, date in appid_to_del:
        del all_appid_data[key][date]

    save_appid_data()
