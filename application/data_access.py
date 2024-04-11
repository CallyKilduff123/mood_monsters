import mysql.connector
from datetime import datetime


def get_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        # password="password",
        database="mood_monsters"
    )
    return mydb
