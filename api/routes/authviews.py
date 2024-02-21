from flask_restx import Namespace, Resource, fields
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import Conflict, BadRequest

from ..models.models import User

auth_namespace=Namespace('auth', description="Definitions of Auth routes")

# signup request model
signup_model=auth_namespace.model(
    'SignUp', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="A email"),
        'password': fields.String(required=True, description="A password"),
    }
)

# login request model
login_model = auth_namespace.model(
    'Login', {  
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password")
    }
)

@auth_namespace.route('/signup')
class SignUp(Resource):

    @auth_namespace.expect(signup_model)
    def post(self):
        """
        Create a new user
        """
        data = request.get_json()

        try:
            new_user = User(
                username=data.get('username'),
                email=data.get('email'),
                password=generate_password_hash(data.get('password'))
            )

            new_user.save()

            response = {
                "message": f"User with email {new_user.email} created"
            }

            return response, HTTPStatus.CREATED
        
        except Exception as e:
            raise Conflict(f"User with email {data.get('email')} exists")
        
        
@auth_namespace.route('/login')
class Login(Resource):

    @auth_namespace.expect(login_model)
    def post(self):
        """
        Login the user and generate a jwt
        """

        data= request.get_json()

        request_email=data.get('email')
        request_password=data.get('password')

        user= User.query.filter_by(email=request_email).first()

        if user is not None and check_password_hash(user.password, request_password):  # user exists in database
            access_token=create_access_token(identity=user.id)

            response={
                'access_token': access_token,
            }

            return response, HTTPStatus.OK
        
        return BadRequest("Invalid username or password")
