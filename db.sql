CREATE TABLE roles(
    username VARCHAR(255) PRIMARY KEY NOT NULL,
    
    --not secure, consider hashing later on 
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'doctor', 'patient'))
);


CREATE TABLE doctors(
    doctor_id VARCHAR(255) PRIMARY KEY NOT NULL,
    username VARCHAR(255) NOT NULL,
    fullname VARCHAR(255) NOT NULL,
    specialization VARCHAR(255),
    experience INTEGER,  
    availability BIT,

    FOREIGN KEY (username) REFERENCES roles(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (specialization) REFERENCES departments(specialization)
        ON DELETE CASCADE
        ON UPDATE CASCADE    
);

CREATE TABLE patients(
    patient_id INTEGER PRIMARY KEY NOT NULL,
    username VARCHAR(255) NOT NULL,
    fullname VARCHAR(255) NOT NULL,
    FOREIGN KEY (username) REFERENCES roles(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE appointments(
    appointment_id VARCHAR(255) NOT NULL PRIMARY KEY,
    patient_id VARCHAR(255) NOT NULL,
    doctor_id VARCHAR(255) NOT NULL,
    
    --keep date in this format: 'DD-MM-YYYY'
    a_date VARCHAR(50) NOT NULL,
    
    --keep time in 24 hour format, no AM/PM: '13:15', '17:35'
    time VARCHAR(50) NOT NULL,
    
    status VARCHAR(50) NOT NULL CHECK (status IN ('Booked','Completed','Cancelled')), 
    
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
 
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE    
);

CREATE TABLE treatments(
    appointment_id VARCHAR(255) NOT NULL PRIMARY KEY,
    diagonosis VARCHAR(255),

    prescription VARCHAR(255),

    notes VARCHAR(255),

    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

);

CREATE TABLE patientHistory(
    visit_no INTEGER NOT NULL PRIMARY KEY,
    visit_type VARCHAR(50) NOT NULL CHECK (visit_type IN ('in-person','online')),
    tests_done VARCHAR(255),
    diagonosis VARCHAR(255),
    prescription VARCHAR(255),
    medicines VARCHAR(255),

    --don't allow cascading on deletion
    FOREIGN KEY (prescription) REFERENCES treatments(prescription)
    ON UPDATE CASCADE,

    FOREIGN KEY (diagonosis) REFERENCES treatments(diagonosis)
    ON UPDATE CASCADE

);

CREATE TABLE departments(
    department_id VARCHAR(255) NOT NULL PRIMARY KEY,
    specialization VARCHAR(255) NOT NULL,
    description VARCHAR(255)
);







PRAGMA foreign_keys = ON;



