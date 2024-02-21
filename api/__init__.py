from flask import Flask
from flask_restx import Api, Resource
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed


from .config.config import config_dict
from .database import db
from .routes.authviews import auth_namespace   
from .routes.notesviews import notes_namespace

# database tables are created here
from .models.models import User, Note, owners_table  


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config) 

    db.init_app(app)

    with app.app_context():
        db.create_all()

    jwt_manager = JWTManager(app)

    authorizations = {
    "Bearer Auth": {  # Use "Bearer Auth" as the security scheme name
        "type": "apiKey",  # Correct the type to "apiKey"
        "in": "header",    # Use "header" instead of "Header"
        "name": "Authorization",
        "description": "Add a JWT with **Bearer <JWT>** to authorize."
        }
    }


    api = Api(app,
            title="Notes API",
            description="A REST API for a notes database",
            authorizations=authorizations,
            security="Bearer Auth"
    )

    api.add_namespace(notes_namespace, path='/notes')
    api.add_namespace(auth_namespace, path='')

    @api.errorhandler(NotFound)
    def not_found(error):
        return {
            "error": "Method Not allowed",
            "message": "Not allowed"
            }, 404

    @api.errorhandler(MethodNotAllowed)
    def methods_not_allowed(error):
        return {
            "error": "Method Not allowed",
            "message": "Not allowed"
            }, 405
        
    return app