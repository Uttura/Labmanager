from flask import render_template, flash, redirect, url_for, request
from Lm.forms import LoginForm, RegisterForm
from Lm import app, db
from Lm.models import User
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/")
def home():
    return render_template('home.html')
@app.route("/labs", methods=['GET'])
def labs():
    return render_template('labs.html')
@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        phashed = generate_password_hash(form.password.data)
        username = form.username.data
        email = form.email.data
        user = User(username=username,email=email, password=phashed)
        db.session.add(user)
        db.session.commit()
        flash('Registered Sucessfully!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', form= form)    