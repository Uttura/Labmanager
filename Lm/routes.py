from flask import render_template, flash, redirect, url_for, request,abort
from flask_login import login_user, login_required, logout_user, current_user
from Lm.forms import LoginForm, RegisterForm, LabForm, FlagForm
from Lm import app, db
from Lm.models import User, Lab, Flag
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@app.route("/")
@login_required
def home():
    total_labs = Lab.query.filter_by(user_id=current_user.id).count()
    labs = Lab.query.filter_by(user_id=current_user.id, status='Active').all()
    pwned_labs = Lab.query.filter_by(user_id=current_user.id, status='pwned').count()
    total_flags = Flag.query.join(Lab).filter(Lab.user_id==current_user.id).count()
    account_days = (datetime.utcnow()-current_user.date_joined).days
    recent_labs = Lab.query.filter_by(user_id = current_user.id).order_by(Lab.date_started.desc()).limit(5).all()
    return render_template('home.html', total_labs=total_labs,labs=labs,boxes_pwned=pwned_labs,flags_captured=total_flags, today_date = datetime.utcnow().day, today_month = datetime.utcnow().strftime('%B'),username=current_user.username,account_days=account_days, recent_labs=recent_labs, session_count = len(labs))

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
@app.route("/labs/<int:lab_id>", methods=['GET'])
@login_required
def labs_view(lab_id):
    lab = Lab.query.filter_by(user_id=current_user.id,id = lab_id).first()
    if lab== None:
        abort(404)
    flag = Flag.query.filter_by(lab_id=lab_id).all()
    
    form = FlagForm()
    return render_template('view_lab.html',lab=lab,form=form,flag=flag)

@app.route("/labs/<int:lab_id>/add_flag", methods=['POST'])
@login_required
def add_flag(lab_id):
    form = FlagForm()
    lab=Lab.query.filter_by(user_id=current_user.id,id=lab_id).first()
    if lab:
        if form.validate_on_submit():
            flags = Flag(flag_value=form.flag_value.data,flag_type=form.flag_type.data, lab_id=lab_id)
            db.session.add(flags)
            db.session.commit()
            flash('Flag added sucessfuly!', 'success')
            return redirect(url_for('labs_view',lab_id=lab_id))
        else:
            flash('Flag value is required.', 'danger')
            return redirect(url_for('labs_view', lab_id=lab_id))
    else:
        abort(403)

@app.route("/flags/<int:flag_id>/delete")
@login_required
def delete_flag(flag_id):
    flag = Flag.query.join(Lab).filter(flag_id==flag_id,Lab.user_id==current_user.id).first()
    if flag:
        db.session.delete(flag)
        db.session.commit()
        return redirect(url_for('labs_view',lab_id=flag.lab_id))
    else:
        abort(403)

        


@app.route("/labs/<int:lab_id>/update", methods=['GET','POST'])
@login_required
def labs_update(lab_id):
    lab=Lab.query.filter_by(user_id=current_user.id,id=lab_id).first()
    if lab== None:
        abort(404)
    form = LabForm(obj=lab)
    if request.method == 'GET':
        if lab.platform not in [choice[0] for choice in form.platform.choices if choice[0] != 'Other']:
            form.platform.data = 'Other'
            form.other_platform.data = lab.platform
        if lab.os not in (choice[0] for choice in form.os.choices if choice[0] != 'Other'):
            form.os.data = 'Other'
            form.other_os.data = lab.os
    if form.validate_on_submit():
        if form.platform.data == 'Other':
            lab.platform = form.other_platform.data
        else:
            lab.platform = form.platform.data
        if form.os.data == 'Other':
            lab.os = form.other_os.data
        else:
            lab.os = form.os.data
        lab.name = form.name.data
        lab.difficulty = form.difficulty.data
        lab.ip_address = form.ip_address.data
        lab.notes = form.notes.data
        lab.url = form.url.data
        db.session.commit()
        return redirect(url_for('labs_view',lab_id=lab_id))
    return render_template('add_lab.html',form=form,edit_mode=True)
    

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