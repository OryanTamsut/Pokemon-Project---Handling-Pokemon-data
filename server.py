import json
import requests
import queries

from flask import Flask, Response, request

app = Flask(__name__)


@app.route('/')
def index():
    return "Server is up"


@app.route('/updateType', methods=['PUT'])
def update_type():
    pokemon_name = request.args.get("name")
    if pokemon_name is None:
        return Response(json.dumps({"err": "require url parameter: name"}), 400)
    else:
        types = requests.get(url=f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/', verify=False).json().get('types')
        types_array = []
        if types is not None:
            for type in types:
                types_array.append(type['type']['name'])
            queries.update_types(pokemon_name, types_array)
            return Response(json.dumps({"success": "types added"}), 200)
        else:
            return Response(json.dumps({"err": "not found types"}), 500)


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
    trainer_name = request.args.get("trainer")
    pokemon_name = request.args.get("pokemon")
    if trainer_name is None or pokemon_name is None:
        return Response(json.dumps({"err": "require url parameter"}), 400)
    result = queries.delete_pokemon(str(trainer_name), str(pokemon_name))
    if result is False:
        return Response(json.dumps({"err": "not found"}), 500)
    return Response(json.dumps({"success:": "deleted"}), 200)


@app.route('/addPokemon', methods=['POST'])
def add_pokemon():
    pokemon_id = request.args.get("id")
    pokemon_name = request.args.get("name")
    pokemon_height = request.args.get("height")
    pokemon_weight = request.args.get("weight")
    if pokemon_id is None or pokemon_name is None or pokemon_height is None or pokemon_weight is None:
        return Response(json.dumps({"err": "require url parameter"}), 400)
    result = queries.add_pokemon(str(pokemon_id), str(pokemon_name), str(pokemon_height), str(pokemon_weight))
    if result is False:
        return Response(json.dumps({"err": "failed"}), 500)
    return Response(json.dumps({"success:": "posted"}), 200)
    return Response(json.dumps({"pokimons": pokemons}), 200)


if __name__ == '__main__':
    app.run(port=5555)
