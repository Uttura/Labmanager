from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
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
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    return app, db,csrf,login_manager
load_dotenv()
app,db,csrf, login_manager = create_app()
from Lm import models
@login_manager.user_loader
def load_user(user_id):
      return User.query.get(user_id)
with app.app_context():
        db.create_all()
from Lm.routes import *