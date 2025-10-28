from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Role(db.Model):
    __tablename__ = 'roles'

    username = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.String(50),
        nullable=False,
        check_constraint="role IN ('admin', 'doctor', 'patient')"
    )


    doctor = db.relationship('Doctor', back_populates='role', uselist=False, cascade='all, delete')
    patient = db.relationship('Patient', back_populates='role', uselist=False, cascade='all, delete')

class Department(db.Model):
    __tablename__ = 'departments'

    department_id = db.Column(db.String(255), primary_key=True, nullable=False)
    specialization = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))


    doctors = db.relationship('Doctor', back_populates='department', cascade='all, delete')

class Doctor(db.Model):
    __tablename__ = 'doctors'

    doctor_id = db.Column(db.String(255), primary_key=True, nullable=False)
    username = db.Column(db.String(255), db.ForeignKey('roles.username', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    fullname = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(255), db.ForeignKey('departments.specialization', ondelete='CASCADE', onupdate='CASCADE'))
    experience = db.Column(db.Integer)
    availability = db.Column(db.Boolean)


    role = db.relationship('Role', back_populates='doctor')
    department = db.relationship('Department', back_populates='doctors')
    appointments = db.relationship('Appointment', back_populates='doctor', cascade='all, delete')

class Patient(db.Model):
    __tablename__ = 'patients'

    patient_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(255), db.ForeignKey('roles.username', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    fullname = db.Column(db.String(255), nullable=False)


    role = db.relationship('Role', back_populates='patient')
    appointments = db.relationship('Appointment', back_populates='patient', cascade='all, delete')

class Appointment(db.Model):
    __tablename__ = 'appointments'

    appointment_id = db.Column(db.String(255), primary_key=True, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    doctor_id = db.Column(db.String(255), db.ForeignKey('doctors.doctor_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    a_date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    status = db.Column(
        db.String(50),
        nullable=False,
        check_constraint="status IN ('Booked','Completed','Cancelled')"
    )


    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')
    treatment = db.relationship('Treatment', back_populates='appointment', uselist=False, cascade='all, delete')

class Treatment(db.Model):
    __tablename__ = 'treatments'

    appointment_id = db.Column(db.String(255), db.ForeignKey('appointments.appointment_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    diagonosis = db.Column(db.String(255))
    prescription = db.Column(db.String(255))
    notes = db.Column(db.String(255))


    appointment = db.relationship('Appointment', back_populates='treatment')
    patient_histories = db.relationship('PatientHistory', back_populates='treatment')

class PatientHistory(db.Model):
    __tablename__ = 'patientHistory'

    visit_no = db.Column(db.Integer, primary_key=True, nullable=False)
    visit_type = db.Column(
        db.String(50),
        nullable=False,
        check_constraint="visit_type IN ('in-person','online')"
    )
    tests_done = db.Column(db.String(255))
    diagonosis = db.Column(db.String(255), db.ForeignKey('treatments.diagonosis', onupdate='CASCADE'))
    prescription = db.Column(db.String(255), db.ForeignKey('treatments.prescription', onupdate='CASCADE'))
    medicines = db.Column(db.String(255))


    treatment = db.relationship('Treatment', back_populates='patient_histories', foreign_keys=[prescription])
