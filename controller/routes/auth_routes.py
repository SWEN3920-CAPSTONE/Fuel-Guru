from flask import Blueprint
from config import app
from controller.routes.token import admin_required


auth = Blueprint('auth_api',__name__)

@auth.route('/signup', methods=['POST'])
def signup():
    """
    Endpoint for signup
    
    Body:
        - username (str)
        - password (str)
        - email (str)
        - firstname (str)
        - lastname (str)
    
    Returns with message:
        - 201 if successful and a JWT to be stored in the client-side
        - 400 if the body sent with the request was malformed
        - 409 if the username or email are already used
        - 500 If the server failed to carry out the request along 
    """
    pass

@auth.route('/signup/manager',methods=['POST'])
@admin_required
def add_gasstation_manager():
    """
    Endpoint for specialised signup for gas station managers
    
    Body:
        - username (str)
        - password (str)
        - email (str)
        - firstname (str)
        - lastname (str)
    
    Returns with message:
        - 201 if successful and a JWT to be stored in the client-side
        - 400 if the body sent with the request was malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not authorized to
        - 500 If the server failed to carry out the request 
    """
    pass


@auth.route('/signin', methods=['POST'])
def signin():
    """
    Endpoint for signin
    
    Body:
        - username or email (str)
        - password (str)
    
    Returns with message:
        - 200 if successful and a JWT to be stored in the client-side
        - 400 if the body sent with the request was malformed
        - 404 if the user + password combo doesnt exist
        - 500 If the server failed to carry out the request
    """
    pass


@auth.route('/logout', methods=['POST'])
def logout():
    """
    Endpoint for log out
    
    Returns with message:
        - 200 if successful and a JWT to be stored in the client-side
        - 400 if the body sent with the request was malformed
        - 404 if the user + password combo doesnt exist
        - 500 If the server failed to carry out the request
    """
    pass

app.register_blueprint(auth,url_prefix='/auth')
