import requests
from werkzeug.wrappers import response

url = "http://127.0.0.1:5555"


# test 1
def test_update_types():
    pass


def test_get_pokemons_by_types():
    pokemons = requests.get(url=f'{url}/getPokemonByType?type=normal').json()
    pokemons = pokemons.get('pokemons')
    assert "eevee" in pokemons
    result = requests.put(url=f'{url}/updateType?name=eevee')
    assert result.status_code == 200


def test_update_pokemon_types():
    result = requests.put(url=f'{url}/updateType?name=venusaur')
    assert result.status_code == 200
    pokemons = requests.get(url=f'{url}/getPokemonByType?type=poison').json().get('pokemons')
    assert "venusaur" in pokemons
    pokemons = requests.get(url=f'{url}/getPokemonByType?type=grass').json().get('pokemons')
    assert "venusaur" in pokemons


test_get_pokemons_by_types()
test_update_pokemon_types()


#     add_pokemon = requests.post(url=f'{url}/addPokemon/',
#                             json={"id": 193, "name": "yanma", "height": 12, "weight": 380}).json()
# assert add_pokemon is True

# assert "yanma" in pokemons
# pokemons = requests.get(url=f'{url}/getPokemonByType?type=bug').jso   n().get('flying')
