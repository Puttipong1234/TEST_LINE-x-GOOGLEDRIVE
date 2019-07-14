from datetime import datetime
import sqlite3
from sqlite3 import Error
 
from app import db
        
        
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    uri = db.Column(db.String(100), unique=False)
    file_id = db.Column(db.String(100), unique=False)

    Submenus= db.relationship('Submenu', backref='menu')

    def __init__(self,name,uri,file_id):
        self.name = name
        self.uri = uri
        self.file_id = file_id

class Submenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    uri = db.Column(db.String(100), unique=False)
    file_id = db.Column(db.String(100), unique=False)
    Menu_id = db.Column(db.Integer,db.ForeignKey('menu.id'))

    def __init__(self,name,uri,file_id,menu):
        self.name = name
        self.uri = uri
        self.file_id = file_id
        self.menu = menu
    # Files_id = db.Column(db.Integer, db.ForeignKey('file.id'))
    Files = db.relationship('File', backref = 'submenu')
    

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    size = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uri = db.Column(db.String(200),unique=False)
    file_id = db.Column(db.String(100), unique=False)

    Submenu_id = db.Column(db.Integer,db.ForeignKey('submenu.id'))
    def __init__(self,name,uri,file_id,submenu):
        self.name = name
        self.uri = uri
        self.file_id = file_id
        self.submenu = submenu


def init_db():
    db.create_all()