from flask import Flask, render_template, request
from flask import current_app as app
from application.models import Role, User
from .temp import *

from flask_security import login_required

@app.route("/")
def login():
    return render_template('pages.html')

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
