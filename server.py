import json
import requests
import queries

from flask import Flask, Response, request

app = Flask(__name__)


@app.route('/')
def index():
    return "Server is up"


@app.route('/update_type', methods=['PUT'])
def update_type():
    pokemon_name = request.args.get("name")
    if pokemon_name is None:
        return Response(json.dumps({"err": "require url parameter: name"}), 400)
    else:
        types = requests.get(url=f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/').json().get('types')
        types_array = []
        if types is not None:
            for type in types:
                types_array.append(type['type']['name'])
            queries.update_types(pokemon_name,types_array)
            return Response(json.dumps({"succes": "types added"}), 200)
        else:
            return Response(json.dumps({"err": "not found types"}), 500)
if __name__ == '__main__':
    app.run(port=5555)
