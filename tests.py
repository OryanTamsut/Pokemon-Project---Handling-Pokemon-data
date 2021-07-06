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


# test 1
def test_get_pokemons_by_types():
    pokemons = requests.get(url=f'{url}/getPokemonByType?type=normal').json()
    pokemons = pokemons.get('pokemons')
    assert "eevee" in pokemons
    result = requests.put(url=f'{url}/updateType?name=eevee')
    assert result.status_code == 200


# test 3
def test_update_pokemon_types():
    result = requests.put(url=f'{url}/updateType?name=venusaur')
    assert result.status_code == 200
    pokemons = requests.get(url=f'{url}/getPokemonByType?type=poison').json().get('pokemons')
    assert "venusaur" in pokemons
    pokemons = requests.get(url=f'{url}/getPokemonByType?type=grass').json().get('pokemons')
    assert "venusaur" in pokemons


# test 7
def test_evolve():
    # try evolve pokemon that can't be evolved
    result = requests.put(url=f'{url}/evolve', json={"pokemon_name": "pinsir", "trainer_name": "Whitney"})
    assert result.status_code != 200

    # try evolve pokemon that not owned by this trainer
    result = requests.put(url=f'{url}/evolve', json={"pokemon_name": "spearow ", "trainer_name": "Archie"})
    assert result.status_code != 200

    # evolve pokemon
    result = requests.put(url=f'{url}/evolve', json={"pokemon_name": "oddish", "trainer_name": "Whitney"})
    assert result.status_code == 200 and result.json().get('success') == "upgrade successfully to gloom"

    # try evolve it again- will fail
    result = requests.put(url=f'{url}/evolve', json={"pokemon_name": "oddish", "trainer_name": "Whitney"})
    assert result.status_code == 400 and result.json().get('err') == "this pokemon is not owned by this traniner"

    # check that gloom is in the Whitney's pokemons
    pokemons = requests.get(url=f'{url}/getPokemonsByTrainer?trainer=Whitney').json().get('pokimons')
    assert "gloom" in pokemons

    # check raichu and pikachu is in Whitney's pokemons
    pokemons = requests.get(url=f'{url}/getPokemonsByTrainer?trainer=Whitney').json().get('pokimons')
    assert "pikachu" in pokemons and "raichu" in pokemons
    # evolve pikachu
    result = requests.put(url=f'{url}/evolve', json={"pokemon_name": "pikachu", "trainer_name": "Whitney"})
    assert result.status_code == 200 and result.json().get(
        'success') == "upgrade successfully to raichu, the pokemon already exist"
