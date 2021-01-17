from typing import Dict, List, Tuple


def sort_hotels_by_countries_and_cities(hotels: List[Dict]) -> Dict:
    """
    Get list of hotels and returns dict of this data:
    Dict structure:
    {'Country's name': {'City's name': [hotels]} }
    :param hotels:
    :return:
    """
    hotels_dict = {}
    for hotel in hotels:
        if hotel["Country"] not in hotels_dict:
            hotels_dict[hotel["Country"]] = {hotel["City"]: []}
        elif hotel["City"] not in hotels_dict[hotel["Country"]]:
            hotels_dict[hotel["Country"]][hotel["City"]] = []
        hotels_dict[hotel["Country"]][hotel["City"]].append(hotel)
    return hotels_dict


def choose_biggest_cities(hotels_dict: Dict) -> List[Tuple]:
    """
    Accept structured data and returns List[(country, biggest city), ...)
    :param hotels_dict:
    :return: List[Tuple]
    """
    list_of_biggest_cities = []
    for country in hotels_dict:
        list_of_biggest_cities.append(
            (
                country,
                max(
                    hotels_dict[country],
                    key=lambda city: len(hotels_dict[country][city]),
                ),
            )
        )

    return list_of_biggest_cities
