import json

from Post_processing.post_process import (
    get_city_and_day_with_highest_temp,
    get_city_and_day_with_highest_temp_delta,
    get_city_and_day_with_lowest_temp,
    get_city_with_highest_all_days_delta,
)

from Weather.weather_forecast import get_min_and_max_temp_per_day

import pytest


@pytest.fixture()
def centers():
    with open("all_cities_centers.json", "r") as f:
        return json.load(f)


@pytest.fixture()
def big_cities():
    return [
        ("GB", "London"),
        ("ES", "Barcelona"),
        ("IT", "Milan"),
        ("FR", "Paris"),
        ("NL", "Amsterdam"),
        ("AT", "Vienna"),
        ("US", "Houston"),
    ]


def test_get_min_and_max_temp_per_day(centers):
    centers["GB"]["London"]["Weather"]["Historical"][0]["hourly"][0]["temp"] = 500
    centers["GB"]["London"]["Weather"]["Historical"][0]["hourly"][1]["temp"] = -100
    data = get_min_and_max_temp_per_day(centers["GB"]["London"]["Weather"])
    assert sorted(data, key=lambda x: x["max"])[-1]["max"] == 500
    assert sorted(data, key=lambda x: x["min"])[0]["min"] == -100


def test_get_city_and_day_with_highest_temp(centers, big_cities):
    centers["GB"]["London"]["Weather"]["Historical"][0]["hourly"][0]["temp"] = 100
    data = get_city_and_day_with_highest_temp(centers, big_cities)
    assert data[2] == 100
    assert data[0] == "London"


def test_get_city_and_day_with_lowest_temp(centers, big_cities):
    centers["GB"]["London"]["Weather"]["Historical"][0]["hourly"][0]["temp"] = -100
    data = get_city_and_day_with_lowest_temp(centers, big_cities)
    assert data[2] == -100
    assert data[0] == "London"


def test_get_city_and_day_with_highest_temp_delta(centers, big_cities):
    centers["GB"]["London"]["Weather"]["Historical"][0]["hourly"][0]["temp"] = -100
    centers["GB"]["London"]["Weather"]["Historical"][0]["hourly"][1]["temp"] = 100
    data = get_city_and_day_with_highest_temp_delta(centers, big_cities)
    assert data[2] == 200
    assert data[0] == "London"


def test_get_city_with_highest_all_days_delta(centers, big_cities):
    centers["GB"]["London"]["Weather"]["Historical"][0]["hourly"][0]["temp"] = -100
    centers["GB"]["London"]["Weather"]["Historical"][-1]["hourly"][0]["temp"] = 100
    data = get_city_with_highest_all_days_delta(centers, big_cities)
    assert data[1] == 200
    assert data[0] == "London"
