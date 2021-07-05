from configure import connection


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
            query = "select name " \
                    "from types t,pokemon p " \
                    f"where t.id =p.id and t.type='{type}'"
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


def update_types(name, types):
    try:
        with connection.cursor() as cursor:
            query_get_id_name = "select id " \
                                "from pokemon " \
                                f"where name=\"{name}\""
            cursor.execute(query_get_id_name)
            id = cursor.fetchall()[0]['id']
            for type in types:
                query_is_exist = f'select * from types where id={id} and type="{type}" '
                cursor.execute(query_is_exist)
                result = cursor.fetchall()
                if len(result) == 0:
                    query_insert_types = 'INSERT into types ( id, type) ' \
                                         f'values ({id}, "{type}")'
                    try:
                        cursor.execute(query_insert_types)
                    except(Exception)as e:
                        print(e)
            connection.commit()
    except(Exception) as e:
        print(e)

