from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
def create_app():
    app =Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///labmanager.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    db = SQLAlchemy(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app()
from Lm.routes import *