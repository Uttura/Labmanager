from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from Lm.forms import LoginForm, RegisterForm
from Lm import app, db
from Lm.models import User, Lab, Flag
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/")
@login_required
def home():
    total_labs = Lab.query.filter_by(user_id=current_user.id).count()
    active_labs = Lab.query.filter_by(user_id=current_user.id, status='in-progress').count()
    total_flags = Flag.query.join(Lab).filter(Lab.user_id==current_user.id).count()

    return render_template('home.html', total_labs=total_labs, active_labs=active_labs, total_flags=total_flags)
@login_required
@app.route("/labs", methods=['GET','POST'])
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
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
              if check_password_hash(user.password,form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('home'))
              else:
                flash("Username or Password is incorrect.")
        else:
            flash("Username or Password is incorrect.")
        
    return render_template('login.html', form= form)
@app.route("/logout")
def logout():
    logout_user()
    flash("You have been Logged Out.")
    return redirect(url_for('home'))