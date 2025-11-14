from flask import Flask, render_template, request
from flask import current_app as app
from application.models import Role, User, Doctor
from application.database import db
from .temp import *

from flask_security import login_required, hash_password

from flask_security import current_user

@app.route("/", methods=['GET','POST'])
@app.route("/dashboard", methods=['GET','POST'])
@login_required
def dashboard():
    if current_user.id==1:
        #admin
        #search
        #add

        return render_template('dashboards/admin_dashboard.html')

    elif current_user.roles==2:
        #doctor
        pass
    else:
        #patient
        pass

@app.route("/add-doctor", methods=['POST'])
@login_required
def add_doctor():
    if current_user.id != 1:
        return "Unauthorized", 403
    
    name = request.form.get('fname')
    specialization = request.form.get('spec')
    email = request.form.get('email')
    password = request.form.get('password')
    
    doctor_role = Role.query.filter_by(name='doctor').first()
    
    new_user = User(email=email, password=hash_password(password), active=True, fs_uniquifier=email)
    new_user.roles.append(doctor_role)
    db.session.add(new_user)
    db.session.commit()
    
    new_doctor = Doctor(name=name, specialization=specialization, email=email)
    db.session.add(new_doctor)
    db.session.commit()
    
    return render_template('dashboards/admin_dashboard.html')

@app.route("/help")
def help():
    return render_template('pages.html', page_name="Help", main="WILL FILL POST DEVELOPMENT", help_active="active")

@app.route("/about")
def about():
    return render_template('pages.html', page_name="about", main="A PROJECT WEB APP FOR HOSPITAL MANAGEMENT, IIT MADRAS", about_active="active")


@app.route("/admin")
@login_required
def admin():
    return render_template('admin.html')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
