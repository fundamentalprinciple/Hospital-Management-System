from flask import Flask, render_template, request, redirect
from flask import current_app as app
from application.models import Role, User, Doctor, Patient
from application.database import db
from .temp import *

from flask_security import login_required, hash_password

from flask_security import current_user
from flask_security.signals import user_registered
from flask import request


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
@login_required
def dashboard():
    # Admin Dashboard
    if current_user.id == 1:
        doctors = Doctor.query.order_by(Doctor.name).all()
        patients = Patient.query.order_by(Patient.name).all()
        return render_template('dashboards/admin_dashboard.html', doctors=doctors, patients=patients)
    # Doctor Dashboard
    elif any(role.name == 'doctor' for role in current_user.roles):
        doctor = Doctor.query.filter_by(email=current_user.email).first()
        doctor_name = doctor.name if doctor and doctor.name else current_user.email
        return render_template('dashboards/doctor_dashboard.html', doctor_name=doctor_name)
    # Patient Dashboard
    else:
        patient = Patient.query.filter_by(email=current_user.email).first()
        patient_name = patient.name if patient and patient.name else current_user.email
        return render_template(
            'dashboards/patient_dashboard.html',
            patient_name=patient_name,
            page_name="Patient Dashboard",
            script="",
        )

@app.route('/edit-patient', methods=['POST'])
@login_required
def edit_patient():
    if current_user.id != 1:
        return "Unauthorized", 403
    patient_id = request.form.get('patient_id')
    name = request.form.get('name')
    email = request.form.get('email')
    if not patient_id:
        return "Missing patient id", 400
    patient = Patient.query.get(patient_id)
    if not patient:
        return "Patient not found", 404
    old_email = patient.email
    patient.name = name
    patient.email = email
    
    user = User.query.filter_by(email=old_email).first()
    if user:
        user.email = email
        user.fs_uniquifier = email
    db.session.commit()
    doctors = Doctor.query.order_by(Doctor.name).all()
    patients = Patient.query.order_by(Patient.name).all()
    return render_template('dashboards/admin_dashboard.html', doctors=doctors, patients=patients)

@app.route('/delete-patient', methods=['POST'])
@login_required
def delete_patient():
    if current_user.id != 1:
        return "Unauthorized", 403
    patient_id = request.form.get('patient_id')
    if not patient_id:
        return "Missing patient id", 400
    patient = Patient.query.get(patient_id)
    if not patient:
        return "Patient not found", 404
    
    user = User.query.filter_by(email=patient.email).first()
    if user:
        db.session.delete(user)
    db.session.delete(patient)
    db.session.commit()
    doctors = Doctor.query.order_by(Doctor.name).all()
    patients = Patient.query.order_by(Patient.name).all()
    return render_template('dashboards/admin_dashboard.html', doctors=doctors, patients=patients)

@app.route("/doctor-dashboard", methods=['GET'])
@login_required
def doctor_dashboard():
    doctor = Doctor.query.filter_by(email=current_user.email).first()
    doctor_name = doctor.name if doctor and doctor.name else current_user.email
    return render_template('dashboards/doctor_dashboard.html', doctor_name=doctor_name)

@app.route("/patient-dashboard", methods=['GET'])
@login_required
def patient_dashboard():
    patient = Patient.query.filter_by(email=current_user.email).first()
    patient_name = patient.name if patient and patient.name else current_user.email
    return render_template(
        'dashboards/patient_dashboard.html',
        patient_name=patient_name,
        page_name="Patient Dashboard",
        script="",
    )

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

@app.route('/blacklist-patient', methods=['POST'])
@login_required
def blacklist_patient():
    if current_user.id != 1:
        return "Unauthorized", 403
    patient_id = request.form.get('patient_id')
    if not patient_id:
        return "Missing patient id", 400
    patient = Patient.query.get(patient_id)
    if not patient:
        return "Patient not found", 404
    user = User.query.filter_by(email=patient.email).first()
    if user:
        user.active = False
        db.session.commit()
    doctors = Doctor.query.order_by(Doctor.name).all()
    patients = Patient.query.order_by(Patient.name).all()
    return render_template('dashboards/admin_dashboard.html', doctors=doctors, patients=patients)

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


@app.route('/after-login')
@login_required
def after_login():
    # Admin
    if current_user.id == 1:
        return redirect('/')

    # Doctor
    if any(role.name == 'doctor' for role in current_user.roles):
        return redirect('/')

    # Patient
    return redirect('/')


@user_registered.connect
def _on_user_registered(sender, user, form_data=None, **extra):
    try:
        name = None
        if form_data and isinstance(form_data, dict):
            name = form_data.get('name')
        if not name:
            name = request.form.get('name')

        if not name:
            return

        if not Patient.query.filter_by(email=user.email).first():
            p = Patient(name=name, email=user.email)
            db.session.add(p)
            db.session.commit()
    except Exception:
        db.session.rollback()
