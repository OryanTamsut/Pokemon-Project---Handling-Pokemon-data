import json
import requests
import queries

from flask import Flask, Response, request

app = Flask(__name__)
url_get_pokemon = "https://pokeapi.co/api/v2/pokemon"

@app.route('/')
def index():
    return "Server is up"

def update_type(pokemon_name):
    types = requests.get(url=f'{url_get_pokemon}/{pokemon_name}/', verify=False).json()
    if types is None:
        return False, "pokemon not exist in API"
    types = types.get('types')
    types_array = []
    if types is not None:
        for type in types:
            types_array.append(type['type']['name'])
        is_success = queries.update_types(pokemon_name, types_array)
        return is_success
    return False, "pokemon's type not exist in API"
    
@app.route('/updateType', methods=['PUT'])
def update_type_route():
    pokemon_name = request.args.get("name")
    if pokemon_name is None:
        return Response(json.dumps({"err": "require url parameter: name"}), 400)
    else:
        is_success = update_type(pokemon_name)
        if is_success[0]:
            return Response(json.dumps({"success": "types added"}), 200)
        else:
            return Response(json.dumps({"err": is_success[1]}), 500)


@app.route('/getPokemonByType', methods=['GET'])
def get_pokemon_by_type():
    type = request.args.get("type")
    if type is None:
        return Response(json.dumps({"err": "require url parameter: type"}), 400)
    else:
        pokemons = queries.find_by_type(type)
        return Response(json.dumps({"pokemons": pokemons}), 200)


@app.route('/getTrainersByPokemon', methods=['GET'])
def get_trainers_by_pokemon():
    pokemon_name = request.args.get("name")
    if pokemon_name is None:
        return Response(json.dumps({"err": "require url parameter: name"}), 400)
    else:
        trainers = queries.find_owners(pokemon_name)
        return Response(json.dumps({"trainers": trainers}), 200)


@app.route('/getPokemonsByTrainer', methods=['GET'])
def get_pokemons_by_trainer():
    trainer_name = request.args.get("trainer")
    if trainer_name is None:
        return Response(json.dumps({"err": "require url parameter: trainer"}), 400)
    pokemons = queries.find_roster(str(trainer_name))
    if pokemons is None:
        return Response(json.dumps({"err": "not found pokemons"}), 500)
    return Response(json.dumps({"pokimons:": pokemons}), 200)


@app.route('/deletePokemons', methods=['DELETE'])
def delete_pokemons_by_trainer():
    trainer_name = request.get_json().get("trainer")
    pokemon_name = request.get_json().get("pokemon")
    if trainer_name is None or pokemon_name is None:
        return Response(json.dumps({"err": "require url parameter"}), 400)
    result = queries.delete_pokemon(str(trainer_name), str(pokemon_name))
    if result is False:
        return Response(json.dumps({"err": "not found"}), 500)
    return Response(json.dumps({"success:": "deleted"}), 200)


@app.route('/addPokemon', methods=['POST'])
def add_pokemon():
    body = request.get_json()
    pokemon_id = body.get("id")
    pokemon_name = body.get("name")
    pokemon_height = body.get("height")
    pokemon_weight = body.get("weight")
    if pokemon_id is None or pokemon_name is None or pokemon_height is None or pokemon_weight is None:
        return Response(json.dumps({"err": "require body parameter: id, name. height, weight"}), 400)
    result = queries.add_pokemon(str(pokemon_id), str(pokemon_name), str(pokemon_height), str(pokemon_weight))
    is_pokemon_in_api = requests.get(url=f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/', verify=False).json()
    if is_pokemon_in_api is None:
        return Response(json.dumps({"success:": "posted"}), 200)
    is_success = update_type(pokemon_name)
    if not result or not is_success:
        return Response(json.dumps({"err": "failed"}), 500)
    return Response(json.dumps({"success:": "posted"}), 200)


@app.route('/evolve', methods=['PUT'])
def evolve():
    pokemon_name = request.get_json().get("pokemon_name")
    trainer_name = request.get_json().get("trainer_name")
    pokemon_data = requests.get(url=f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/', verify=False).json()
    if pokemon_data is None:
        return Response(json.dumps({"err": "failed- not found pokemon in API"}), 500)
    id = pokemon_data.get('id')
    species = pokemon_data.get('species')
    evolution_chain = requests.get(url=species.get('url'), verify=False).json().get('evolution_chain')
    chain = requests.get(url=evolution_chain.get('url'), verify=False).json().get('cain')
    while chain.get('species').get('name'):
        chain = chain.get('evolves_to')[0]
    if len(chain.get('evolves_to')) == 0:
        return Response(json.dumps({"success": "not have a new version"}), 200)
    new_name = chain.get('evolves_to')[0].get('species').get('name')
    new_pokemon = requests.get(url=f'https://pokeapi.co/api/v2/pokemon/{new_name}/', verify=False).json()
    is_success = queries.add_pokemon(new_pokemon.get('id'), new_name, new_pokemon.get('height'),
                                     new_pokemon.get('weight'))
    if not is_success:
        return Response(json.dumps({"err": "failed- could not upgrade pokemon"}), 500)
    is_success = update_type(new_name)
    if not is_success:
        return Response(json.dumps({"err": "failed- could not upgrade pokemon"}), 500)
    is_success = queries.update_own_pokemon(trainer_name, id, new_pokemon.get('id'))
    if not is_success:
        return Response(json.dumps({"err": "failed- could not upgrade pokemon"}), 500)
    return Response(json.dumps({"success": "not have a new version"}), 200)


if __name__ == '__main__':
    app.run(port=5555)
