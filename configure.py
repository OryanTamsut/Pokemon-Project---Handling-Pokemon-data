import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="db_pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

port = 5555

url_get_pokemon = "https://pokeapi.co/api/v2/pokemon"

url_server = "http://127.0.0.1:" + str(port)