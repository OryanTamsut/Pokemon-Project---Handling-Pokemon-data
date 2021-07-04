import json
from configure import connection


def load_data():
    trainers = []
    pairs = []
    with open('./pokemon_data.json', 'r') as file:
        pokemons = json.load(file)
    for pokemon in pokemons:
        for owner in pokemon['ownedBy']:
            trainers.append({"name": f'{owner["name"]}', 'town': f'{owner["town"]}'})
            pairs.append({"pokemon_id": pokemon["id"], "own_name": owner["name"]})
    try:
        with connection.cursor() as cursor:
            for pokemon in pokemons:
                query = 'INSERT into pokemon (id, name, type, height, weight) ' \
                        f'values ({pokemon["id"]},"{pokemon["name"]}", "{pokemon["type"]}",' \
                        f' {pokemon["height"]}, {pokemon["weight"]})'
                try:
                    cursor.execute(query)
                except:
                    pass
            for trainer in trainers:
                query = 'INSERT into trainer ( name, town) ' \
                        f'values ("{trainer["name"]}", "{trainer["town"]}")'
                try:
                    cursor.execute(query)
                except:
                    pass
            for pair in pairs:
                query = 'INSERT into ownership (owner_name,pokemon_id) ' \
                        f'values ("{pair["own_name"]}", {pair["pokemon_id"]})'
                try:
                    cursor.execute(query)
                except(Exception) as e:
                    print(e)
        connection.commit()
    except(Exception) as e:
        print(e)


if __name__ == '__main__':
    load_data()
