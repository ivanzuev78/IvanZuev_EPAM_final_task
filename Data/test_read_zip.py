import pytest

from Data.read_zip import filter_hotel


@pytest.mark.parametrize(
    "hotel",
    [
        [1, "Some Hotel", "US", "London", "41.79735", "-87.72327"],
        ['1234134', "Some Hotel", "US", "London", "41.79735", "-87.72327"],
        ['12.34134E+10', "Some Hotel", "US", "London", "41.79735", "-87.72327"],

    ],
)
def test_hotel_filter_good_input(hotel):
    assert filter_hotel(hotel)




def test_hotel_filter_bad_id():
    hotel = ['bad id', "Some Hotel", "US", "London", "41.79735", "-87.72327"]
    assert filter_hotel(hotel) is None


def test_hotel_filter_bad_latitude():
    hotel = ['1', "Some Hotel", "US", "London", "bad Latitude", "-87.72327"]
    assert filter_hotel(hotel) is None


def test_hotel_filter_bad_longitude():
    hotel = ['1', "Some Hotel", "US", "London", "41.79735", "bad Longitude"]
    assert filter_hotel(hotel) is None

@pytest.mark.parametrize(
    "hotel",
    [

        ['1', "", "US", "London", "41.79735", "-87.72327"],
        ['1', "Some Hotel", "", "London", "41.79735", "-87.72327"],
        ['1', "Some Hotel", "US", "", "41.79735", "-87.72327"],

    ],
)
def test_hotel_filter_some_data_is_empty(hotel):
    assert filter_hotel(hotel) is None

