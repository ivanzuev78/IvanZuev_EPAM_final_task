from Data.read_zip import filter_hotel

import pytest


@pytest.fixture(autouse=True)
def column_names():
    return {"Id": 0, "Name": 1, "Country": 2, "City": 3, "Latitude": 4, "Longitude": 5}


@pytest.mark.parametrize(
    "hotel",
    [
        [1, "Some Hotel", "US", "London", "41.79735", "-87.72327"],
        ["1234134", "Some Hotel", "US", "London", "41.79735", "-87.72327"],
        ["12.34134E+10", "Some Hotel", "US", "London", "41.79735", "-87.72327"],
    ],
)
def test_hotel_filter_good_input(hotel, column_names):
    assert filter_hotel(hotel, column_names)


def test_hotel_filter_bad_id(column_names):
    hotel = ["bad id", "Some Hotel", "US", "London", "41.79735", "-87.72327"]
    assert filter_hotel(hotel, column_names) is None


def test_hotel_filter_bad_latitude(column_names):
    hotel = ["1", "Some Hotel", "US", "London", "bad Latitude", "-87.72327"]
    assert filter_hotel(hotel, column_names) is None


def test_hotel_filter_bad_longitude(column_names):
    hotel = ["1", "Some Hotel", "US", "London", "41.79735", "bad Longitude"]
    assert filter_hotel(hotel, column_names) is None


@pytest.mark.parametrize(
    "hotel",
    [
        ["1", "", "US", "London", "41.79735", "-87.72327"],
        ["1", "Some Hotel", "", "London", "41.79735", "-87.72327"],
        ["1", "Some Hotel", "US", "", "41.79735", "-87.72327"],
    ],
)
def test_hotel_filter_some_data_is_empty(hotel, column_names):
    assert filter_hotel(hotel, column_names) is None
