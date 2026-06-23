from flask import Flask
from flask_wtf.csrf import CSRFProtect
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
def create_app():
    app =Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    db = SQLAlchemy(app)
    csrf = CSRFProtect(app)
    return app, db,csrf
load_dotenv()
app,db,csrf = create_app()
from Lm import models
with app.app_context():
        db.create_all()
from Lm.routes import *