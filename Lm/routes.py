from flask import render_template, flash, redirect, url_for, request
from Lm.forms import LoginForm, RegisterForm
from Lm import app

@app.route("/")
def home():
    return render_template('home.html')
@app.route("/labs", methods=['GET'])
def labs():
    return render_template('labs.html')
@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit:
        username = form.username.data
        email = form.email.data
        flash('Registered Sucessfully!', 'success')
        return redirect(url_for('home'))
    if request.method == 'GET':
        form.username.data = 'Tester'
        form.email.data = 'tester@gmail.com'
    return render_template('register.html', form=form)
