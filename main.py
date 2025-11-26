import os
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import seed_departments

from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
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

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    
    with app.app_context():
        db.create_all()
    '''
        if not security.datastore.find_user(email="test@me.com"):
            security.datastore.create_user(email="test@me.com", password=hash_password("password"))
            db.session.commit()
    '''

    with app.app_context():
        roles = ['admin','doctor','patient']
        for name in roles:
            if not Role.query.filter_by(name=name).first():
                db.session.add(Role(name=name))
                db.session.commit()
    
        admin_user = User.query.filter_by(email='admin@admin.com').first()
        if not admin_user:
            admin_user = User(email='admin@admin.com', password=hash_password(os.getenv('Admin')), active=True, fs_uniquifier='')
            db.session.add(admin_user)
            db.session.commit()

        seed_departments()    


    app.app_context().push()
    return app, api

app, api = create_app()

from application.controllers import *

from application.api import UserAPI
api.add_resource(UserAPI, "/api/user/<string:username>", "/api/user")



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
