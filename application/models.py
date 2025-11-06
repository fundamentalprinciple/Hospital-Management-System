'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
'''

from flask_security import UserMixin, RoleMixin


from .database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(255))
    hash = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    role = db.Column(db.String(255), db.ForeignKey('role.role'))

    def __repr__(self):
        return f"User({self.id},{self.username},{self.role})"

class Role(db.Model, RoleMixin):
    role = db.Column(db.String(255), primary_key=True)
        
    __table_args__ = (
                db.CheckConstraint('role IN ("admin", "doctor", "patient") ' , name='role_check'),
            )

    def __repr__(self):
        return f"Roles({self.role})"

