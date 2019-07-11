from app import db
from datetime import datetime

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    Files = db.relationship('File', backref = 'menu')

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    size = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uri = db.Column(db.String(200),nullable=False,unique=False)

    Menu_id = db.Column(db.Integer,db.ForeignKey('Menu.id'))