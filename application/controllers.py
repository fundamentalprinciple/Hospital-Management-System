from flask import Flask, render_template, request
from flask import current_app as app
from application.models import Role, User
from .temp import *

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
