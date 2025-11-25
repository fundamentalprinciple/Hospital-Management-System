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

class Doctor(db.Model):
    __tablename__='doctor'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)


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
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(32), nullable=False, default='Booked')  
    reason = db.Column(db.String(255))  
    notes = db.Column(db.Text)  
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    patient = db.relationship('Patient', backref=db.backref('appointments', lazy=True))
    doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy=True))    
