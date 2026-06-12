from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
def create_app():
    app =Flask(__name__)
    app.config['SECRET_KEY'] = os.evniron.get['SECRET_KEY']
    db = SQLAlchemy(app)
    with app.app_context():
        db.create_all()
    return app
load_dotenv()
app = create_app()
from Lm.routes import *