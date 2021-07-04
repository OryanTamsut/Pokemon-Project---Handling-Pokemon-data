from configure import connection

#oryan
def heaviest_pokemon():
    try:
        with connection.cursor() as cursor:
            query = "select name from pokemon where weight in(select max(weight) from pokemon)"
            cursor.execute(query)
            result = cursor.fetchall()
            return result[0]['name']
    except(Exception) as e:
        print(e)


def find_by_type(type):
    try:
        with connection.cursor() as cursor:
            query = f"SELECT name FROM pokemon WHERE type = '{type}'"
            cursor.execute(query)
            result = cursor.fetchall()
            result2 = []
            for name in result:
                result2.append(name['name'])
            return result2
    except(Exception) as e:
        print(e)


def find_owners(pokemon_name):
    try:
        with connection.cursor() as cursor:
            query = "select owner_name " \
                    "from ownership ,pokemon " \
                    f"where pokemon_id= id and name=\"{pokemon_name}\""
            cursor.execute(query)
            result = cursor.fetchall()
            result2 = []
            for name in result:
                result2.append(name['owner_name'])
            return result2
    except(Exception) as e:
        print(e)


def find_roster(trainer_name):
    try:
        with connection.cursor() as cursor:
            query = "select name " \
                    "from ownership ,pokemon " \
                    f"where pokemon_id= id and owner_name=\"{trainer_name}\""
            cursor.execute(query)
            result = cursor.fetchall()
            result2 = []
            for name in result:
                result2.append(name['name'])
            return result2
    except(Exception) as e:
        print(e)


def finds_most_owned():
    try:
        with connection.cursor() as cursor:
            query = "select name from " \
                    "(select pokemon_id, count(*) as count " \
                    "from ownership " \
                    "group by pokemon_id) as ob1, pokemon " \
                    "where count in (select max(count) from " \
                    "(select pokemon_id, count(*) as count " \
                    "from ownership " \
                    "group by pokemon_id) as ob2) and id=pokemon_id "
            cursor.execute(query)
            result = cursor.fetchall()
            result2 = []
            for name in result:
                result2.append(name['name'])
            return result2
    except(Exception) as e:
        print(e)

