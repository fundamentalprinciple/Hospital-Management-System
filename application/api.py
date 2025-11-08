from flask_restful import Resource
from flask_restful import fields, marshal_with

from application.database import db
from application.models import User

output_fields = {
        "user_id": fields.Integer,
        "username": fields.String,
        "roles": fields.String
    }

class UserAPI(Resource):
    @marshal_with(output_fields)
    def get(self, username):
        user = db.session.query(User).filter(User.username == username).first()        
        
        if user:
            return user
        else:
            return {}, 404

    def put(self, username):
        pass
    
    def delete(self, username):
        pass
    
    def post(self):
        pass
  
