from Data.sort_hotels_data import (
    choose_biggest_cities,
    sort_hotels_by_countries_and_cities,
)


def test_sort_hotels_by_countries_and_cities():

    hotels_list = [
        {"Id": 1, "Country": "US", "City": "New-York"},
        {"Id": 2, "Country": "US", "City": "New-York"},
        {"Id": 9, "Country": "GB", "City": "London"},
    ]

    hotels_dict = {
        "US": {
            "New-York": [
                {"Id": 1, "Country": "US", "City": "New-York"},
                {"Id": 2, "Country": "US", "City": "New-York"},
            ]
        },
        "GB": {"London": [{"Id": 9, "Country": "GB", "City": "London"}]},
    }
    assert sort_hotels_by_countries_and_cities(hotels_list) == hotels_dict


def test_choose_biggest_cities():
    hotels_dict = {
        "US": {
            "New-York": [
                {"Id": 1, "Country": "US", "City": "New-York"},
                {"Id": 2, "Country": "US", "City": "New-York"},
            ],
            "Washington": [{"Id": 3, "Country": "US", "City": "Washington"}],
        },
        "GB": {"London": [{"Id": 4, "Country": "GB", "City": "London"}]},
    }

    assert choose_biggest_cities(hotels_dict) == [("US", "New-York"), ("GB", "London")]
