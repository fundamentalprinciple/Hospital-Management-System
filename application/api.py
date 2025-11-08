from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse

from application.database import db
from application.models import User
from application.validation import NotFoundError, BusinessValidationError

output_fields = {
        "user_id": fields.Integer,
        "username": fields.String,
        "roles": fields.String
    }

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username')

class UserAPI(Resource):

    @marshal_with(output_fields)
    def get(self, username):
        user = db.session.query(User).filter(User.username == username).first()        
        
        if user:
            return user
        else:
            raise NotFoundError(status_code=404) 

    def put(self, username):
        pass
    
    def delete(self, username):
        pass
    
    def post(self):
        args = create_user_parser.parse_args()
        username = args.get("username", None)
        
        if username is None:
            raise BusinessValidationError(status_code=400, error_code='BE1001', error_message="username is required")
        
        pass         


