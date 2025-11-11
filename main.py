import os
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from flask_bcrypt import Bcrypt

from application.models import User, Role

from flask_restful import Resource, Api


app = None
api = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    
    
    api = Api(app)
    
    db.init_app(app)
    
    
    bcrypt = Bcrypt(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    
    with app.app_context():
        db.create_all()

    app.app_context().push()


    hashed = bcrypt.generate_password_hash("pass2").decode('utf-8')
    with app.app_context():
        user_datastore.create_user(email="test2@x.com", password=hashed)
        db.session.commit()
        User.query.all()

    print(LocalDevelopmentConfig.SQLALCHEMY_DATABASE_URI)
    return app, api

app, api = create_app()

from application.controllers import *

from application.api import UserAPI
api.add_resource(UserAPI, "/api/user/<string:username>", "/api/user")



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
