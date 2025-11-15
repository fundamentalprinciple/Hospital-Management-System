from flask import Flask, render_template, request
from flask import current_app as app
from application.models import Role, User, Doctor
from application.database import db
from .temp import *

from flask_security import login_required, hash_password

from flask_security import current_user


def _get_doctors_info():
    """Return a list of (Doctor, active_bool) tuples for all doctors."""
    docs = Doctor.query.order_by(Doctor.name).all()
    info = []
    for d in docs:
        user = User.query.filter_by(email=d.email).first()
        active = bool(user.active) if user and user.active is not None else False
        info.append((d, active))
    return info


def _get_doctors_info():
    """Return a list of (Doctor, active_bool) tuples for all doctors."""
    docs = Doctor.query.order_by(Doctor.name).all()
    info = []
    for d in docs:
        user = User.query.filter_by(email=d.email).first()
        active = bool(user.active) if user and user.active is not None else False
        info.append((d, active))
    return info

@app.route("/", methods=['GET','POST'])
@app.route("/dashboard", methods=['GET','POST'])
@login_required
def dashboard():
    # Admin Dashboard
    if current_user.id==1:
        #search
        #add
        doctors = Doctor.query.order_by(Doctor.name).all()
        return render_template('dashboards/admin_dashboard.html', doctors=doctors)
    # Doctor Dashboard
    elif any(role.name == 'doctor' for role in current_user.roles):
        # try to find the doctor's full name from the Doctor model using the user's email
        doctor = Doctor.query.filter_by(email=current_user.email).first()
        doctor_name = doctor.name if doctor and doctor.name else current_user.email
        return render_template('dashboards/doctor_dashboard.html', doctor_name=doctor_name)
    # Patient Dashboard
    else:
        return render_template('dashboards/patient_dashboard.html')

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
    
    doctors = Doctor.query.order_by(Doctor.name).all()
    return render_template('dashboards/admin_dashboard.html', doctors=doctors)


@app.route('/edit-doctor', methods=['POST'])
@login_required
def edit_doctor():
    if current_user.id != 1:
        return "Unauthorized", 403

    doctor_id = request.form.get('doctor_id')
    name = request.form.get('fname')
    specialization = request.form.get('spec')
    email = request.form.get('email')
    password = request.form.get('password')

    if not doctor_id:
        return "Missing doctor id", 400

    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return "Doctor not found", 404

    old_email = doctor.email
    doctor.name = name
    doctor.specialization = specialization
    doctor.email = email

    # update linked user if email changed or password provided
    user = User.query.filter_by(email=old_email).first()
    if user:
        user.email = email
        user.fs_uniquifier = email
        if password:
            user.password = hash_password(password)

    db.session.commit()

    return render_template('dashboards/admin_dashboard.html', doctors=Doctor.query.order_by(Doctor.name).all())


@app.route('/delete-doctor', methods=['POST'])
@login_required
def delete_doctor():
    if current_user.id != 1:
        return "Unauthorized", 403

    doctor_id = request.form.get('doctor_id')
    if not doctor_id:
        return "Missing doctor id", 400

    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return "Doctor not found", 404

    # delete associated user if exists
    user = User.query.filter_by(email=doctor.email).first()
    if user:
        db.session.delete(user)

    db.session.delete(doctor)
    db.session.commit()

    return render_template('dashboards/admin_dashboard.html', doctors=Doctor.query.order_by(Doctor.name).all())


@app.route('/blacklist-doctor', methods=['POST'])
@login_required
def blacklist_doctor():
    if current_user.id != 1:
        return "Unauthorized", 403

    doctor_id = request.form.get('doctor_id')
    if not doctor_id:
        return "Missing doctor id", 400

    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return "Doctor not found", 404

    user = User.query.filter_by(email=doctor.email).first()
    if user:
        user.active = False
        db.session.commit()

    return render_template('dashboards/admin_dashboard.html', doctors=Doctor.query.order_by(Doctor.name).all())

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
