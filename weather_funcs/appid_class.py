import datetime
import json
import os
from pathlib import Path
from typing import Dict, Optional

from dateutil import parser


class AppId:
    """
    To get weather from openweathermap.org you need actual
    Requests are limited. Only 1000 per day per one appid
    This class helps you to work with lots of appid and use actual appid
    appid_data format is:
    {'appid': { 'YYYY-MM-DD" : numb of usage this day } }
    """

    def __init__(self, path_to_appid_json: Path, appid: str = None):
        self.path_to_appid_json = path_to_appid_json
        self.appid_data = self.load_appid()
        if appid is not None:
            self.add_appid(appid)
        self.clean_appid_old_date()

    def load_appid(self) -> Dict:
        """
        load all appid from "openweathermap_appid.json"
        """
        if os.path.exists(self.path_to_appid_json):
            try:
                with open(self.path_to_appid_json, "r") as file:
                    appid_data = json.load(file)
                for appid in appid_data:
                    if not isinstance(appid, str):
                        raise ValueError("appid is not 'str'")
                    if not isinstance(appid_data[appid], dict):
                        raise ValueError("appid_data[appid] is not 'dict'")
                    for date in appid_data[appid]:
                        if not isinstance(date, str):
                            raise ValueError("date is not 'str'")
                        if not isinstance(appid_data[appid][date], int):
                            raise ValueError(f"numb of usage {appid} is not 'int'")
                        if appid_data[appid][date] < 0:
                            raise ValueError(f"numb of usage {appid} < 0")
            except Exception:
                # TODO: add message to log
                return {}
        return {}

    def save_appid_data(self) -> None:
        with open(self.path_to_appid_json, "w") as file:
            json.dump(self.appid_data, file, indent=4)

    def get_appid(self) -> Optional[str]:
        """
        Return actual appid
        """
        date = str(datetime.datetime.utcnow().date())

        for appid in self.appid_data:
            if date in self.appid_data[appid]:
                if self.appid_data[appid][date] < 1000:
                    self.appid_data[appid][date] += 1
                    break
            else:
                self.appid_data[appid][date] = 1
                break
        else:
            return None

        if appid:
            self.save_appid_data()
        else:
            # TODO: add message to log
            pass

        return appid

    def add_appid(self, appid: str) -> None:
        """
        Function to add appid to the file and use it
        """
        if appid not in self.appid_data:
            self.appid_data[appid] = {}
            self.save_appid_data()

    def close_appid_for_this_day(self, appid: str) -> None:
        """
        If there are some problems with appid, it can be closed for this day
        """
        self.appid_data[appid][str(datetime.datetime.utcnow().date())] = 1000
        self.save_appid_data()

    def clean_appid_old_date(self):
        """
        Clean "openweathermap_appid.json" by deleting the previous dates
        """
        appid_to_del = []

        for key in self.appid_data:
            for date in self.appid_data[key]:
                if datetime.datetime.utcnow() - parser.parse(date) > datetime.timedelta(
                    1
                ):
                    appid_to_del.append([key, date])

        for key, date in appid_to_del:
            del self.appid_data[key][date]

        self.save_appid_data()
