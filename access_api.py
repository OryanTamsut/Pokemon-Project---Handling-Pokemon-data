import requests
from configure import url_get_pokemon

"""
get pokemon name and get from the api the pokemon's type and update it in the DB
"""


def get_pokemon_types(pokemon_name):
    # get the pokemon data from API
    types = requests.get(url=f'{url_get_pokemon}/{pokemon_name}/', verify=False).json()
    if types is None:
        return False, "pokemon not exist in API"
    # create array of the pokemon types
    types = types.get('types')
    types_array = []
    if types is not None:
        for type in types:
            types_array.append(type['type']['name'])
        return True, types_array
    return False, "pokemon's type not exist in API"


"""
get pokemon name and trainer name and return the next name of the new version
"""


def get_the_new_evolve(pokemon_data, pokemon_name):
    species = pokemon_data.get('species')
    evolution_chain = requests.get(url=species.get('url'), verify=False).json().get('evolution_chain')
    chain = requests.get(url=evolution_chain.get('url'), verify=False).json().get('chain')
    while chain.get('species').get('name') != pokemon_name:
        if len(chain.get('evolves_to')) == 0:
            return {"error": "not have a new version"}, 500
        chain = chain.get('evolves_to')[0]
    if len(chain.get('evolves_to')) == 0:
        return {"error": "not have a new version"}, 500
    return chain.get('evolves_to')[0].get('species').get('name'), 200


"""
get pokemon id or name and return the full data of the pokemon
"""


def get_pokemon_data(pokemon):
    pokemon_data = requests.get(url=f'{url_get_pokemon}/{pokemon}/', verify=False)
    pokemon_data = pokemon_data.json()
    return pokemon_data
