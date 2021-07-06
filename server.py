import json
import queries
from access_api import *

from flask import Flask, Response, request

app = Flask(__name__)


@app.route('/')
def index():
    return "Server is up"


"""
get pokemon name and add his types to DB
expected url: POST "http://127.0.0.1:5555/updateType?name={name}"
return success if add or error if not
"""


@app.route('/updateType', methods=['PUT'])
def update_type_route():
    # check all the parameters sent
    pokemon_name = request.args.get("name")
    if pokemon_name is None:
        return Response(json.dumps({"err": "require url parameter: name"}), 400)
    else:
        # update the pokemon's type and return message if success or if not
        types_array = get_pokemon_types(str(pokemon_name))
        if types_array[0]:
            is_success = queries.update_types(pokemon_name, types_array[1])
            if not is_success[0]:
                return Response(json.dumps({"err": "failed " + is_success[1]}), 500)
            return Response(json.dumps({"success": "types added"}), 200)
        else:
            return Response(json.dumps({"err": types_array[1]}), 500)


"""
get pokemons by type
expected url: GET "http://127.0.0.1:5555/getPokemonByType?type={type}"
return {"pokemons":["Drasna",...]} if success or {"err": err_message} if not
"""


@app.route('/getPokemonByType', methods=['GET'])
def get_pokemon_by_type():
    # check all the parameters sent
    type = request.args.get("type")
    if type is None:
        return Response(json.dumps({"err": "require url parameter: type"}), 400)
    else:
        # get the pokemons that have this type
        pokemons = queries.find_by_type(str(type))
        return Response(json.dumps({"pokemons": pokemons}), 200)


"""
get all the trainers of the pokemon
expected url: GET "http://127.0.0.1:5555/getTrainersByPokemon?name={pokemon_name}"
return {"trainers":["Drasna",...]} if success or {"err": err_message} if not
"""


@app.route('/getTrainersByPokemon', methods=['GET'])
def get_trainers_by_pokemon():
    # check all the parameters sent
    pokemon_name = request.args.get("name")
    if pokemon_name is None:
        return Response(json.dumps({"err": "require url parameter: name"}), 400)
    else:
        # get all the trainers of the Pokemon
        trainers = queries.find_owners(str(pokemon_name))
        return Response(json.dumps({"trainers": trainers}), 200)


"""
get all the pokemons of the trainer 
expected url: GET "http://127.0.0.1:5555/getPokemonsByTrainer?trainer={trainer_name}"
return {"pokimons":["Drasna",...]} if success or {"err": err_message} if not
"""


@app.route('/getPokemonsByTrainer', methods=['GET'])
def get_pokemons_by_trainer():
    # check all the parameters sent
    trainer_name = request.args.get("trainer")
    if trainer_name is None:
        return Response(json.dumps({"err": "require url parameter: trainer"}), 400)
    # get all the pokemons of the trainer
    pokemons = queries.find_roster(str(trainer_name))
    if pokemons is None:
        return Response(json.dumps({"err": "not found pokemons"}), 500)
    return Response(json.dumps({"pokimons": pokemons}), 200)


"""
delete pokemon of a trainer
expected url: DELETE "http://127.0.0.1:5555/deletePokemons"
body:{"trainer":trainer_name, "pokemon":pokemon_name}
return {"success:": "deleted"} if success or {"err": err_message} if not
"""


@app.route('/deletePokemons', methods=['DELETE'])
def delete_pokemons_by_trainer():
    # check all the parameters sent
    trainer_name = request.get_json().get("trainer")
    pokemon_name = request.get_json().get("pokemon")
    if trainer_name is None or pokemon_name is None:
        return Response(json.dumps({"err": "require url parameter: trainer, pokemon"}), 400)
    # delete the pokemon
    result = queries.delete_pokemon(str(trainer_name), str(pokemon_name))
    if result is False:
        return Response(json.dumps({"err": "not found"}), 500)
    return Response(json.dumps({"success:": "deleted"}), 200)


"""
add pokemon to the DB and add his type also
expected url: POST "http://127.0.0.1:5555/addPokemon"
body:{"id":pokemon_id, "name":pokemon_name, "height":pokemon_height,"weight":pokemon_weight}
return {"success:": "posted"} if success or {"err": err_message} if not
"""


@app.route('/addPokemon', methods=['POST'])
def add_pokemon():
    # check all the parameters sent
    body = request.get_json()
    pokemon_id = body.get("id")
    pokemon_name = body.get("name")
    pokemon_height = body.get("height")
    pokemon_weight = body.get("weight")
    if pokemon_id is None or pokemon_name is None or pokemon_height is None or pokemon_weight is None:
        return Response(json.dumps({"err": "require body parameter: id, name. height, weight"}), 400)
    # add the pokemon to the DB
    result = queries.add_pokemon(str(pokemon_id), str(pokemon_name), str(pokemon_height), str(pokemon_weight))
    if not result[0]:
        return Response(json.dumps({"err": result[1]}), 500)
    is_pokemon_in_api = get_pokemon_data(pokemon_name)
    if is_pokemon_in_api is None:
        return Response(json.dumps({"success:": "posted"}), 200)
    # update the type's of the pokemon
    types_array = get_pokemon_types(pokemon_name)
    if types_array[0]:
        is_success = queries.update_types(pokemon_name, types_array[1])
        if not is_success[0]:
            return Response(json.dumps({"err": "failed " + is_success[1]}), 500)
    else:
        return Response(json.dumps({"err": "failed " + types_array[1]}), 500)
    return Response(json.dumps({"success:": "posted"}), 200)


"""
upgrade pokemon to the next version (if have next, else- stay in his version)
expected url: PUT "http://127.0.0.1:5555/evolve"
body:{"pokemon_name":pokemon_name, "trainer_name":trainer_name}
return {"success": "not have a new version"} or {"success": "upgrade successfully"} if success or {"err": err_message} if not
"""


@app.route('/evolve', methods=['PUT'])
def evolve():
    # check all the parameters sent
    pokemon_name = request.get_json().get("pokemon_name")
    trainer_name = request.get_json().get("trainer_name")
    if pokemon_name is None or trainer_name is None:
        return Response(json.dumps({"err": "require body parameter: pokemon_name,trainer_name "}), 400)
    # get the next version of the pokemon
    pokemon_data = get_pokemon_data(pokemon_name)
    if pokemon_data is None:
        return Response(json.dumps({"err": "failed- not found pokemon in API"}), 500)
    id = pokemon_data.get('id')
    if queries.check_exist_owner_pokemon(trainer_name, id) is False:
        return {"err": "this pokemon is not owned by this traniner"}, 400

    result = get_the_new_evolve(pokemon_data, pokemon_name)
    if result[1] != 200:
        return Response(json.dumps(result[0]), result[1])
    new_name = result[0]
    # get the new pokemon data and add it to the DB
    new_pokemon = get_pokemon_data(new_name)
    is_success = queries.add_pokemon(new_pokemon.get('id'), new_name, new_pokemon.get('height'),
                                     new_pokemon.get('weight'))
    if not is_success[0] and is_success[1] != "pokemon already exist":
        return Response(json.dumps({"err": "failed- could not upgrade pokemon " + is_success[1]}), 500)
    types_array = get_pokemon_types(pokemon_name)
    if types_array[0]:
        is_success = queries.update_types(pokemon_name, types_array[1])
        if not is_success[0]:
            return Response(json.dumps({"err": "failed- could not upgrade pokemon: " + is_success[1]}), 500)
        # update the pokemon's owner that now he have a new version
        is_success = queries.update_own_pokemon(trainer_name, id, new_pokemon.get('id'))
        if not is_success[0]:
            return Response(json.dumps({"err": "failed- could not upgrade pokemon " + is_success[1]}), 500)
        if is_success[1] == "already exist":
            return Response(
                json.dumps({"success": "upgrade successfully to " + new_name + ", the pokemon already exist"}),
                200)
        else:
            return Response(json.dumps({"success": "upgrade successfully to " + new_name}),
                            200)
    else:
        return Response(json.dumps({"err": "failed- could not upgrade pokemon: " + types_array[1]}), 500)
