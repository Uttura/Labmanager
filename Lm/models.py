from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from Lm import db
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable= False)
    password = db.Column(db.String(120), nullable = False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    labs = db.relationship('Lab', backref= 'owner', lazy = True)
    github = db.relationship('Github', backref= 'owner', lazy = True)
class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable = False)
    platform = db.Column(db.String(120), nullable = False)
    os = db.Column(db.String(60), nullable=True)
    difficulty = db.Column(db.String(15), nullable=True, default='Easy')
    ip_address = db.Column(db.String(45), nullable=True)
    date_started = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_pwned = db.Column(db.DateTime, nullable=True, default=None)
    notes = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    status = db.Column(db.String(20), nullable = False, default='Active')
    flags = db.relationship('Flag', backref='lab', lazy = True, cascade='all, delete-orphan')
class Flag(db.Model):
    flag_id = db.Column(db.Integer, primary_key = True)
    flag_value = db.Column(db.String(200), nullable = False)
    flag_type = db.Column(db.String(20),nullable=False)
    captured_at = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable = False)

class Github(db.Model):
    github_owner = db.Column(db.String(100),nullable=True)
    github_repo = db.Column(db.String(100),nullable=True)
    github_path = db.Column(db.String(100),nullable=True)
    github_token = db.Column(db.String(200),nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

