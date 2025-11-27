from datetime import date, time
from flask_security import UserMixin, RoleMixin
from uuid import uuid4
from .database import db


roles_users = db.Table(
        'roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    )


class User(db.Model, UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)

    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    fs_uniquifier = db.Column(db.String, unique=True, nullable=False, default=lambda: uuid4().hex)


class Role(db.Model, RoleMixin):
    __tablename__='role'
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255))


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)
    doctors_registered = db.Column(db.Integer, default=0)
    extra_info = db.Column(db.Text)

    doctors = db.relationship('Doctor', backref='department', lazy=True)


#harcoded departments
def seed_departments():
    departments = [
        Department(id=1, name="Cardiology", description="Specializes in diagnosing and treating heart and blood-vessel disorders, including heart disease, arrhythmias, hypertension, and heart failure."),
        Department(id=2, name="Oncology", description="Focuses on the diagnosis and treatment of cancer through chemotherapy, radiation therapy, immunotherapy, and coordinated cancer care."),
        Department(id=3, name="Emergency Department", description="Provides immediate evaluation and treatment of urgent and life-threatening conditions such as trauma, stroke, heart attack, and severe infections."),
        Department(id=4, name="Pediatrics", description="Delivers medical care for infants, children, and adolescents, addressing growth, development, diseases, and preventive health services."),
        Department(id=5, name="Obstetrics & Gynecology", description="Cares for women’s reproductive health, pregnancy, childbirth, and disorders of the female reproductive system."),
        Department(id=6, name="Neurology", description="Diagnoses and treats disorders of the brain, spinal cord, and nervous system—such as epilepsy, stroke, migraines, and neurodegenerative diseases."),
        Department(id=7, name="Orthopedics", description="Manages conditions of the bones, joints, muscles, ligaments, and tendons, including fractures, arthritis, and sports injuries."),
        Department(id=8, name="Radiology", description="Uses imaging technologies—such as X-ray, CT, MRI, and ultrasound—to diagnose and sometimes treat medical conditions."),
        Department(id=9, name="General Surgery", description="Performs surgical procedures on organs such as the stomach, intestines, gallbladder, and thyroid, as well as trauma and emergency surgeries."),
        Department(id=10, name="Intensive Care Unit", description="Provides continuous, specialized care for critically ill patients requiring close monitoring, advanced life support, and complex treatments.")
    ]
    for dept in departments:
        existing = Department.query.filter_by(id=dept.id).first()
        if not existing:
            db.session.add(dept)
    db.session.commit()


class Doctor(db.Model):
    __tablename__='doctor'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)


class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)


class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    shift = db.Column(db.String(16), nullable=False)  # 'morning' or 'evening'
    time = db.Column(db.Time, nullable=True)  # Optional, can be set to None
    status = db.Column(db.String(32), nullable=False, default='Booked')  
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    patient = db.relationship('Patient', backref=db.backref('appointments', lazy=True))
    doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy=True))    


class PatientHistory(db.Model):
    __tablename__ = 'patient_history'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    visit_no = db.Column(db.Integer, nullable=False)
    visit_type = db.Column(db.String(255))
    tests_done = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    medicines = db.Column(db.Text)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    patient = db.relationship('Patient', backref=db.backref('history', lazy=True))


class Availability(db.Model):
    __tablename__ = 'availability'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    morning = db.Column(db.Boolean, default=False)
    evening = db.Column(db.Boolean, default=False)
    doctor = db.relationship('Doctor', backref=db.backref('availabilities', lazy=True))    