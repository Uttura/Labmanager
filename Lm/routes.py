from flask import render_template
from Lm import app

@app.route("/")
def home():
    return render_template('home.html')
@app.route("/labs", methods=['GET'])
def labs():
    return render_template('labs.html')
