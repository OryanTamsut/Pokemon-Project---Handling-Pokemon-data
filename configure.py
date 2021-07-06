import pymysql

port = 5555

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="DB_Pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
