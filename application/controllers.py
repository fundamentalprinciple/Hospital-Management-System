from flask import url_for, flash
from datetime import date, timedelta
from flask import Flask, render_template, request, redirect
from flask import current_app as app
from application.models import Role, User, Doctor, Patient, Department, Appointment
from application.database import db
from .temp import *

from flask_security import login_required, hash_password

from flask_security import current_user
from flask_security.signals import user_registered
from flask import request


def _get_doctors_info():
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
        departments = Department.query.order_by(Department.name).all()

        appointments = Appointment.query.all()
        def appt_sort_key(appt):

            shift_priority = 0 if (hasattr(appt, 'shift') and appt.shift and appt.shift.lower() == 'morning') else 1
            return (appt.date, shift_priority, appt.id)
        sorted_appointments = sorted(appointments, key=appt_sort_key)

        appt_list = []
        for appt in sorted_appointments:
            doctor = Doctor.query.get(appt.doctor_id)
            dept = Department.query.get(doctor.department_id) if doctor else None
            patient = Patient.query.get(appt.patient_id)
            appt_list.append({
                'id': appt.id,
                'patient_name': patient.name if patient else '',
                'patient_id': patient.id if patient else '',
                'doctor_name': doctor.name if doctor else '',
                'department': dept.name if dept else '',
                'date': appt.date,
                'shift': appt.shift
            })
        return render_template('dashboards/admin_dashboard.html', doctors=doctors, patients=patients, departments=departments, appointments=appt_list)
    
    # Doctor Dashboard
    elif any(role.name == 'doctor' for role in current_user.roles):
        doctor = Doctor.query.filter_by(email=current_user.email).first()
        doctor_name = doctor.name if doctor and doctor.name else current_user.email
        return render_template('dashboards/doctor_dashboard.html', doctor_name=doctor_name)
    
    # Patient Dashboard
    else:
        patient = Patient.query.filter_by(email=current_user.email).first()
        patient_name = patient.name if patient and patient.name else current_user.email
        departments = Department.query.order_by(Department.name).all()
        appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.date).all() if patient else []
        appt_list = []
        for appt in appointments:
            doctor = Doctor.query.get(appt.doctor_id)
            dept = Department.query.get(doctor.department_id) if doctor else None
            appt_list.append({
                'id': appt.id,
                'doctor_name': doctor.name if doctor else '',
                'department': dept.name if dept else '',
                'date': appt.date,
                'shift': appt.shift
            })
        return render_template(
            'dashboards/patient_dashboard.html',
            patient_name=patient_name,
            page_name="Patient Dashboard",
            script="",
            departments=departments,
            appointments=appt_list
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
    appointments = []
    patients = []
    if doctor:
        from application.models import Appointment, Patient, Department

        all_appts = Appointment.query.filter_by(doctor_id=doctor.id).all()
        def appt_sort_key(appt):
            shift_priority = 0 if (hasattr(appt, 'shift') and appt.shift and appt.shift.lower() == 'morning') else 1
            return (appt.date, shift_priority, appt.id)
        sorted_appts = sorted(all_appts, key=appt_sort_key)

        from datetime import date as dtdate
        today = dtdate.today()
        appointments = []
        for appt in sorted_appts:
            if appt.date >= today:
                patient = Patient.query.get(appt.patient_id)
                dept = Department.query.get(doctor.department_id) if doctor else None
                appointments.append({
                    'id': appt.id,
                    'patient_name': patient.name if patient else '',
                    'doctor_name': doctor.name,
                    'department': dept.name if dept else '',
                    'date': appt.date,
                    'shift': appt.shift
                })

        patients = list({Patient.query.get(a.patient_id) for a in all_appts})
    return render_template('dashboards/doctor_dashboard.html', doctor_name=doctor_name, appointments=appointments, patients=patients)


@app.route("/patient-dashboard", methods=['GET'])
@login_required
def patient_dashboard():
    from application.models import Appointment, Doctor, Department
    patient = Patient.query.filter_by(email=current_user.email).first()
    patient_name = patient.name if patient and patient.name else current_user.email
    departments = Department.query.order_by(Department.name).all()

    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.date).all() if patient else []

    appt_list = []
    for appt in appointments:
        doctor = Doctor.query.get(appt.doctor_id)
        dept = Department.query.get(doctor.department_id) if doctor else None
        appt_list.append({
            'id': appt.id,
            'doctor_name': doctor.name if doctor else '',
            'department': dept.name if dept else '',
            'date': appt.date,
            'shift': appt.shift
        })
    return render_template(
        'dashboards/patient_dashboard.html',
        patient_name=patient_name,
        page_name="Patient Dashboard",
        script="",
        departments=departments,
        appointments=appt_list
    )


@app.route("/add-doctor", methods=['POST'])
@login_required
def add_doctor():
    if current_user.id != 1:
        return "Unauthorized", 403
    name = request.form.get('fname')
    email = request.form.get('email')
    password = request.form.get('password')
    department_id = request.form.get('department_id')
    doctor_role = Role.query.filter_by(name='doctor').first()
    new_user = User(email=email, password=hash_password(password), active=True, fs_uniquifier=email)
    new_user.roles.append(doctor_role)
    db.session.add(new_user)
    db.session.commit()
    new_doctor = Doctor(name=name, email=email, department_id=department_id)
    db.session.add(new_doctor)

    department = Department.query.get(department_id)
    if department:
        department.doctors_registered = (department.doctors_registered or 0) + 1
    db.session.commit()
    doctors = Doctor.query.order_by(Doctor.name).all()
    patients = Patient.query.order_by(Patient.name).all()
    departments = Department.query.order_by(Department.name).all()
    return render_template('dashboards/admin_dashboard.html', doctors=doctors, patients=patients, departments=departments)



@app.route('/edit-doctor', methods=['POST'])
@login_required
def edit_doctor():
    if current_user.id != 1:
        return "Unauthorized", 403
    doctor_id = request.form.get('doctor_id')
    name = request.form.get('fname')
    email = request.form.get('email')
    password = request.form.get('password')
    department_id = request.form.get('department_id')
    if not doctor_id:
        return "Missing doctor id", 400
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return "Doctor not found", 404
    old_email = doctor.email
    doctor.name = name
    doctor.email = email
    doctor.department_id = department_id
    user = User.query.filter_by(email=old_email).first()
    if user:
        user.email = email
        user.fs_uniquifier = email
        if password:
            user.password = hash_password(password)
    db.session.commit()
    doctors = Doctor.query.order_by(Doctor.name).all()
    patients = Patient.query.order_by(Patient.name).all()
    departments = Department.query.order_by(Department.name).all()
    return render_template('dashboards/admin_dashboard.html', doctors=doctors, patients=patients, departments=departments)


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

    if doctor.department_id:
        department = Department.query.get(doctor.department_id)
        if department and department.doctors_registered:
            department.doctors_registered = max(0, department.doctors_registered - 1)

    user = User.query.filter_by(email=doctor.email).first()
    if user:
        db.session.delete(user)

    db.session.delete(doctor)
    db.session.commit()

    doctors = Doctor.query.order_by(Doctor.name).all()
    patients = Patient.query.order_by(Patient.name).all()
    departments = Department.query.order_by(Department.name).all()
    return render_template('dashboards/admin_dashboard.html', doctors=doctors, patients=patients, departments=departments)


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

@app.route('/department/<int:dept_id>', methods=['GET'])
@login_required
def department_details(dept_id):
    department = Department.query.get_or_404(dept_id)
    doctors = department.doctors if department else []
    return render_template('dashboards/department.html', department=department, doctors=doctors)


@app.route('/patient_history/<int:patient_id>', methods=['GET'])
@login_required
def patient_history(patient_id):
    from application.models import Patient, PatientHistory
    patient = Patient.query.get_or_404(patient_id)
    history = PatientHistory.query.filter_by(patient_id=patient_id).order_by(PatientHistory.visit_no).all()
    return render_template('dashboards/patient_history.html', patient=patient, history=history)


@app.route('/doctor_schedule', methods=['GET', 'POST'])
@login_required
def doctor_schedule():
    from application.models import Availability
    doctor = Doctor.query.filter_by(email=current_user.email).first()
    if not doctor:
        return "Unauthorized", 403
    if request.method == 'POST':
        slot_date = request.form.get('date')
        slot_type = request.form.get('slot')
        if slot_date and slot_type:
            from datetime import datetime
            slot_date_obj = datetime.strptime(slot_date, "%Y-%m-%d").date()
            avail = Availability.query.filter_by(doctor_id=doctor.id, date=slot_date_obj).first()
            if not avail:
                avail = Availability(doctor_id=doctor.id, date=slot_date_obj)
                db.session.add(avail)

            if slot_type == 'morning':
                avail.morning = not avail.morning
            elif slot_type == 'evening':
                avail.evening = not avail.evening

            if not avail.morning and not avail.evening:
                db.session.delete(avail)
            db.session.commit()

    today = date.today()
    days = []
    avail_lookup = {}
    for avail in Availability.query.filter_by(doctor_id=doctor.id).all():
        avail_lookup[avail.date] = avail
    for i in range(7):
        d = today + timedelta(days=i)
        avail = avail_lookup.get(d)
        days.append({
            'date': d.isoformat(),
            'date_str': d.strftime('%A, %d %B %Y'),
            'morning': avail.morning if avail else False,
            'evening': avail.evening if avail else False
        })
    return render_template('dashboards/doctor_schedule.html', days=days)


@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    from application.models import Doctor, Availability, Appointment, Patient
    from datetime import datetime, timedelta, date
    doctor_id = request.args.get('doctor_id') or request.form.get('doctor_id')
    doctor = Doctor.query.get_or_404(doctor_id)
    patient = Patient.query.filter_by(email=current_user.email).first()
    if not patient:
        return "Unauthorized", 403
    today = date.today()
    days = []
    avail_lookup = {}
    for avail in Availability.query.filter_by(doctor_id=doctor.id).all():
        avail_lookup[avail.date] = avail
    for i in range(7):
        d = today + timedelta(days=i)
        avail = avail_lookup.get(d)
        days.append({
            'date': d.isoformat(),
            'date_str': d.strftime('%A, %d %B %Y'),
            'morning': avail.morning if avail else False,
            'evening': avail.evening if avail else False
        })
    booked = False
    if request.method == 'POST':
        slots = request.form.getlist('slots')
        booked_any = False
        for slot in slots:
            try:
                slot_date, slot_shift = slot.split('|')
                slot_date_obj = datetime.strptime(slot_date, "%Y-%m-%d").date()
                exists = Appointment.query.filter_by(
                    doctor_id=doctor.id,
                    patient_id=patient.id,
                    date=slot_date_obj,
                    shift=slot_shift
                ).first()
                if not exists:
                    appt = Appointment(
                        doctor_id=doctor.id,
                        patient_id=patient.id,
                        date=slot_date_obj,
                        shift=slot_shift
                    )
                    db.session.add(appt)
                    booked_any = True
                else:
                    flash(f'Already booked: {slot_date} {slot_shift}', 'warning')
            except Exception as e:
                flash(f'Error booking slot: {slot}', 'danger')
        if booked_any:
            db.session.commit()
            booked = True
    return render_template(
        'dashboards/schedule.html',
        doctor=doctor,
        days=days,
        booked=booked
    )


@app.route('/cancel-appointment', methods=['POST'])
@login_required
def cancel_appointment():
    from application.models import Appointment
    appt_id = request.form.get('appointment_id')
    appt = Appointment.query.get(appt_id)
    if appt:
        db.session.delete(appt)
        db.session.commit()
    return redirect('/patient-dashboard')

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


@app.route("/help")
def help():
    return render_template('pages.html', page_name="Help", main="WILL FILL POST DEVELOPMENT", help_active="active")


@app.route("/about")
def about():
    return render_template('pages.html', page_name="about", main="A PROJECT WEB APP FOR HOSPITAL MANAGEMENT, IIT MADRAS", about_active="active")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404