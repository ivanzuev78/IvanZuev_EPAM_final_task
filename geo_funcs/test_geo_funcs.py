from geo_funcs.geo_funcs import get_city_center


def test_get_city_center():
    hotels = [
        ["1", "min_latitude", "US", "City", 0, 12.2345],
        ["2", "max_latitude", "US", "City", 90, 42],
        ["3", "min_longitude", "US", "City", 23, 0],
        ["4", "max_longitude", "US", "City", 55, 90],
        ["5", "Name", "US", "City", 78, 74.999],
        ["6", "Name", "US", "City", 33, 59.001],
        ["7", "Name", "US", "City", 89, 12],
    ]
    assert get_city_center(hotels) == (45, 45)
