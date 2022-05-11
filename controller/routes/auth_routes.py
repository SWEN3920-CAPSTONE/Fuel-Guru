from datetime import datetime, timedelta
import json
from pprint import pprint
from flask import Blueprint, jsonify, make_response, request
import jwt
from marshmallow import ValidationError
from config import app, csrf
from controller.routes.token import admin_required, token_required
from controller.validation.schemas import SigninSchema
from model import User


auth = Blueprint('auth_api', __name__)


@auth.route('/signup', methods=['POST'])
@csrf.exempt
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
        - 200 if successful and a JWT to be stored in the client-side
        - 400 if the body sent with the request was malformed
        - 409 if the username or email are already used
        - 500 If the server failed to carry out the request along 
    """
    pass


@auth.route('/signup/manager', methods=['POST'])
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
        - 200 if successful and a JWT to be stored in the client-side
        - 400 if the body sent with the request was malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not authorized to
        - 500 If the server failed to carry out the request 
    """
    pass


@auth.route('/signin', methods=['POST'])
@csrf.exempt
def signin():
    """
    Endpoint for signin

    Body:
        - iden (str):

            Email or user name

        - password (str)

    Returns with message:
        - 200 if successful and a JWT to be stored in the client-side

    Returns with error:
        - 400 if the body sent with the request was malformed
        - 401 if the user + password combo doesnt exist
        - 500 If the server failed to carry out the request
    """
    try:
        data = SigninSchema().load(request.get_json(
            silent=True, force=True) or request.form.to_dict())

        user: User = User.query.filter_by(username=data['iden']).first(
        ) or User.query.filter_by(email=data['iden']).first()

        if user:
            if user.check_password(data['password']):
                expiry_time = app.config.get(
                    'JWT_ACCESS_LIFESPAN').get('hours')

                # Generate the JWT Token
                token = jwt.encode({
                    'id': user.id,
                    'exp': datetime.utcnow() + timedelta(hours=expiry_time),
                }, app.config.get('SECRET_KEY'), algorithm="HS256")

                return jsonify({
                    'message': 'Login Successful',
                    'token': token
                }), 200

        return jsonify(
            {'error': 'Incorrect username or email and password combination'}), 401
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400


@auth.route('/logout', methods=['POST'])
@token_required
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


app.register_blueprint(auth, url_prefix='/auth')
