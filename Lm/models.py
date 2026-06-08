from flask_sqlalchemy import SQLAlchemy
from labmanager.Lm import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable= False)
    password = db.Column(db.String(120), nullable = False)

    labs = db.relationship('Lab', backref= 'owner', lazy = True)
class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lab_name = db.Column(db.String(120), nullable = False)
    lab_organization = db.Column(db.String(120), nullable = False)
    user_id = db.Column(db.Integer, db.Foreign_Key('user.id'), nullable = False)

    flag = db.relationship('Flag', backref='owner', lazy = True)
class Flag(db.M0del):
    flag_id = db.Column(db.Integer, primary_key = True)
    flag_value = db.Coulmn(db.String(200), nullable = False)
    lab_id = db.Column(db.Integer,db.Foreign_key('lab.id'), nullable = False)



