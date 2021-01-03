def sort_hotels_by_countries_and_cities(hotels: list):
    hotels_dict = {}
    for hotel in hotels:
        if hotel["Country"] not in hotels_dict:
            hotels_dict[hotel["Country"]] = {hotel["City"]: []}
        elif hotel["City"] not in hotels_dict[hotel["Country"]]:
            hotels_dict[hotel["Country"]][hotel["City"]] = []
        hotels_dict[hotel["Country"]][hotel["City"]].append(hotel)
    return hotels_dict


def choose_biggest_cities(hotels_dict: dict) -> list:
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
