import os

from flask import Flask
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy

from models import db
from models import Role, Doctor, Patient, Appointment, Treatment, Department, PatientHistory

from temp import *

app=Flask(__name__)


#DB SETUP

current_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(current_dir, "database.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(app)
with app.app_context():
    db.create_all()


#ROUTES

@app.route("/")
@app.route("/login")
def login():
    

    return render_template('auth_info/pages.html', page_name="Login",main=login_main, log_active="active")

@app.route("/register")
def register():
    return render_template('auth_info/pages.html', page_name="Register" ,main=register_main, log_active="active")

@app.route("/help")
def help():
    return render_template('auth_info/pages.html', page_name="Help", main="WILL FILL POST DEVELOPMENT", help_active="active")

@app.route("/about")
def about():
    return render_template('auth_info/pages.html', page_name="about", main="A PROJECT WEB APP FOR HOSPITAL MANAGEMENT, IIT MADRAS", about_active="active")


if __name__=="__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
    
