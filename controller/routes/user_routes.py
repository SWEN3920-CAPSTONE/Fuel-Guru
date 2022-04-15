from flask import Blueprint
from config import app
from controller.routes.token import admin_required, token_required

user_api = Blueprint('user_api', __name__)


@user_api.route('', methods=['DELETE', 'PUT'])
@token_required
def edit_user():
    """
    Endpoint for editing or deleting a user
    
    No body for DELETE
    
    Body for PUT (one of the following):
        - [firstname]
        - [lastname]
        - [email]
        - [password]
    
    Returns with message:
        - 200 if the request was successful
        - 400 if the body was empty for PUT or otherwise malformed
        - 401 if the user making the request isnt logged in
        - 500 for server error
    """
    pass


@user_api.route('/types', methods=['POST', 'PUT', 'GET'])
@admin_required
def user_types():
    """
    Endpoint for handling user types
    
    Body for POST:
        - user_type_name
        
    Body for PUT:
        - user_type name
        - id
        
    Returns with message:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not an admin
        - 500 if there was a server error
    """
    pass

app.register_blueprint(user_api, url_prefix='/users')