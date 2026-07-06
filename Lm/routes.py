from flask import render_template, flash, redirect, url_for, request,abort
from flask_login import login_user, login_required, logout_user, current_user
from Lm.forms import LoginForm, RegisterForm, LabForm
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

@app.route("/labs", methods=['GET'])
@login_required
def labs():
    labs = Lab.query.filter_by(user_id=current_user.id).order_by(Lab.date_started.desc()).all()

    return render_template('labs.html', labs=labs)


@app.route("/labs/new", methods=['GET', 'POST'])
@login_required
def labs_new():
    form = LabForm()
    if form.validate_on_submit():
        if form.platform.data=='Other':
            platform = form.other_platform.data
        else:
            platform = form.platform.data
        if form.os.data=='Other':
            os = form.other_os.data
        else:
            os = form.os.data
        name = form.name.data
        difficulty = form.difficulty.data
        ip_address = form.ip_address.data
        notes = form.notes.data
        url = form.url.data
        user_id=current_user.id
        lab = Lab(name = name, difficulty=difficulty, ip_address=ip_address, notes=notes, url=url, platform=platform, os=os, user_id=user_id)
        db.session.add(lab)
        db.session.commit()
        flash('Lab created!', 'success')
        return redirect(url_for('labs'))
    return render_template('add_lab.html', form=form)
@app.route("/labs/<int:lab_id>", methods=['GET', 'POST'])
@login_required
def labs_view(lab_id):
    lab = Lab.query.filter_by(user_id=current_user.id,id = lab_id).first()
    if lab== None:
        return redirect(abort(404))
    return render_template('view_lab.html',lab=lab)

@app.route("/labs/<int:lab_id>/update")
@login_required
def labs_update(lab_id):
    lab=Lab.query.filter_by(user_id=current_user.id,id=lab_id).first()

@app.route("/labs/<int:lab_id>/delete")
@login_required
def labs_delete(lab_id):
    lab=Lab.query.filter_by(user_id=current_user.id,id=lab_id).first()
    if lab:
        db.session.delete(lab)
        db.session.commit()
        flash('Lab Deleted','fail')
        return redirect(url_for('labs'))
    return render_template('view_lab.html')

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