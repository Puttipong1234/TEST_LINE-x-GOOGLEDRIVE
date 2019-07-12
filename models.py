from datetime import datetime
import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
    return db_file+".sqlite3"
        
        
from app import db
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    Submenus = db.relationship('Submenu', backref = 'Submenu')

class Submenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    Files = db.relationship('File', backref = 'menu')

    Menu_id = db.Column(db.Integer,db.ForeignKey('Menu.id'))
    

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    size = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uri = db.Column(db.String(200),nullable=False,unique=False)

    Submenu_id = db.Column(db.Integer,db.ForeignKey('Submenu.id'))