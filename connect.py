import sqlite3
from app import db

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        db.create_all()
    except Error as e:
        print(e)
    finally:
        conn.close()
    return db_file+".sqlite3"