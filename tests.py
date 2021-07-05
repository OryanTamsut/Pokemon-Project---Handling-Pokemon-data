import requests

url = "http://127.0.0.1:5555"


# test 1
def test_update_types():
    pass


# test 2
def test_add_pokemon():
    # this test can run only one times! (or delete the data that added from the DB)
    # add yanma pokemon to DB
    add_pokemon = requests.post(url=f'{url}/addPokemon',
                                json={"id": 193, "name": "yanma", "height": 12, "weight": 380})

    assert add_pokemon.status_code == 200

    # assert that added to types table that yanma have "bug" in its types
    pokemons = requests.get(url=f'{url}/getPokemonByType?type=bug').json().get('pokemons')
    assert "yanma" in pokemons

    # assert that added to types table that yanma have "flying" in its types
    pokemons = requests.get(url=f'{url}/getPokemonByType?type=flying').json().get('pokemons')
    assert "yanma" in pokemons

    # assert pokemon already exist
    add_pokemon = requests.post(url=f'{url}/addPokemon',
                                json={"id": 193, "name": "yanma", "height": 12, "weight": 380})
    add_pokemon_mess = add_pokemon.json()
    assert add_pokemon.status_code == 500 and add_pokemon_mess.get('err') == "pokemon already exist"


# test 4
def test_get_pokemons_by_owner():
    # get all the pokemon that Dransa have
    pokemons = requests.get(url=f'{url}/getPokemonsByTrainer?trainer=Drasna').json().get('pokimons')
    assert pokemons == ["wartortle", "caterpie", "beedrill", "arbok", "clefairy", "wigglytuff", "persian", "growlithe",
                        "machamp", "golem", "dodrio", "hypno", "cubone", "eevee", "kabutops"]


# test 5
def test_get_owners_by_pokemon():
    # get all the owners of pokemon charmander
    trainers = requests.get(url=f'{url}/getTrainersByPokemon?name=charmander').json().get('trainers')
    assert trainers == ["Giovanni", "Jasmine", "Whitney"]
