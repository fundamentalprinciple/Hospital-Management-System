from flask_security import UserMixin, RoleMixin

from .database import db

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.role'))
                       )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    hash = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    fs_uniquifier = db.Column(db.String, unique=True, nullable=False, default=lambda: uuid4().hex)

    def __repr__(self):
        return f"User({self.id},{self.username},{self.role})"

class Role(db.Model, RoleMixin):
    role = db.Column(db.String(255), primary_key=True)
        
    __table_args__ = (
                db.CheckConstraint('role IN ("admin", "doctor", "patient") ' , name='role_check'),
            )

    def __repr__(self):
        return f"Roles({self.role})"

#db.create_all()
