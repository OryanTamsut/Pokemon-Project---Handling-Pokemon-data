from configure import connection


def heaviest_pokemon():
    try:
        with connection.cursor() as cursor:
            # select the haviest pokemon from DB
            query = "select name from pokemon where weight in(select max(weight) from pokemon)"
            cursor.execute(query)
            result = cursor.fetchall()
            return result[0]['name']
    except(Exception) as e:
        print(e)
        return False


def find_by_type(type):
    try:
        with connection.cursor() as cursor:
            # find all the pokemons where their type equals to the accepted type
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
        return False


def find_owners(pokemon_name):
    try:
        with connection.cursor() as cursor:
            # find all the owners of the accepted pokemon
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
        return False


def find_roster(trainer_name):
    try:
        with connection.cursor() as cursor:
            # find all the pokemons of the accepted trainer
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
        return False


def finds_most_owned():
    try:
        with connection.cursor() as cursor:
            # finds the pokemon that has the most owners
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


def delete_pokemon(trainer, pokemon):
    try:
        with connection.cursor() as cursor:
            # delete the accepted pokemon from the accepted trainer's pokemons list
            query = "delete from ownership " \
                    f"where owner_name = '{trainer}' and pokemon_id in" \
                    f" (select id from pokemon where name = '{pokemon}')"
            cursor.execute(query)
        connection.commit()
    except(Exception) as e:
        return False


def add_pokemon(id, name, height, weight):
    try:
        with connection.cursor() as cursor:
            # validate the accepted pokemon is not in the DB
            query = f'select * from pokemon where id={id}'
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) > 0:
                return False, "pokemon already exist"
            # insert the accepted pokemon into the DB
            query = 'INSERT into pokemon (id, name, height, weight) ' \
                    f'values ({id},"{name}", {height}, {weight})'
            cursor.execute(query)
        connection.commit()
        return True, "success"
    except(Exception) as e:
        return False, e


def update_types(name, types):
    try:
        with connection.cursor() as cursor:
            # get the id of the accepted pokemon
            query_get_id_name = "select id " \
                                "from pokemon " \
                                f"where name=\"{name}\""
            cursor.execute(query_get_id_name)
            id = cursor.fetchall()[0]['id']
            for type in types:
                # for each type in the array, validate the accepted pokemon and the type are not in the types table
                query_is_exist = f'select * from types where id={id} and type="{type}" '
                cursor.execute(query_is_exist)
                result = cursor.fetchall()
                if len(result) == 0:
                    # insert the accepted pokemon and the type to the table
                    query_insert_types = 'INSERT into types ( id, type) ' \
                                         f'values ({id}, "{type}")'
                    try:
                        cursor.execute(query_insert_types)
                    except(Exception)as e:
                        return False, str(e)
            connection.commit()
            return True, "success"
    except(Exception) as e:
        return False, str(e)


def update_own_pokemon(owner_name, pokemon_id_prev, pokemon_id_current):
    try:
        with connection.cursor() as cursor:
            try:
                # validate the pokemon is not update already
                query_check_exist = "select * " \
                                    "from ownership " \
                                    f"where owner_name='{owner_name}' and pokemon_id={pokemon_id_current}"
                cursor.execute(query_check_exist)
                result = cursor.fetchall()
                if len(result) != 0:
                    return True, "already exist"
                # update the pokemon id
                query_update_ownership = "UPDATE ownership " \
                                         f"SET pokemon_id = {pokemon_id_current} " \
                                         f"WHERE owner_name='{owner_name}' and pokemon_id={pokemon_id_prev};"
                cursor.execute(query_update_ownership)
                connection.commit()
                return True, "success"
            except(Exception)as e:
                return False, str(e)
    except(Exception) as e:
        print(e)
        return False, str(e)


def check_exist_owner_pokemon(owner_name, pokemon_id):
    try:
        with connection.cursor() as cursor:
            try:
                # validate the accepted pair exists
                query_update_ownership = "SELECT * " \
                                         "FROM pokemon.ownership " \
                                         f"where owner_name='{owner_name}' and pokemon_id={pokemon_id};"
                cursor.execute(query_update_ownership)
                result = cursor.fetchall()
                if len(result) > 0:
                    return True
                return False
            except:
                return False
    except:
        return False
