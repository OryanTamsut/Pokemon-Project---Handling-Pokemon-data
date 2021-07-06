import pymysql
from flask import Flask, Response, request

app = Flask(__name__)

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="db_pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

port = 5555
