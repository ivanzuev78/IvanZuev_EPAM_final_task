import pandas as pd

from geo_funcs.geo_funcs import get_top_city_df


def test_get_city_center():
    cities_series = pd.Series(["City"], index=["US"])
    hotels = pd.DataFrame(
        {
            "Country": ["US" for _ in range(7)],
            "City": ["City" for _ in range(7)],
            "Latitude": [0, 90, 23, 55, 78, 33, 89],
            "Longitude": [0, 89, 23, 55, 78, 33, 90],
        }
    )

    result = get_top_city_df(cities_series, hotels)

    assert result["Latitude"][0] == 45
    assert result["Longitude"][0] == 45
