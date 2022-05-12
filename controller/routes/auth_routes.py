from datetime import datetime
from hashlib import sha256

from config import app, csrf, db
from controller.routes.token import admin_required, gen_access_refresh_token, token_required
from controller.utils import get_request_body
from controller.validation.schemas import SigninSchema, SignupSchema
from flask import Blueprint, jsonify, request, g
from marshmallow import ValidationError
from model import User, UserType, InvalidToken

from flask_jwt_extended import get_jwt

auth = Blueprint('auth_api', __name__)

# TODO test


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

    Returns with error:
        - 400 if the body sent with the request was malformed
        - 409 if the username or email are already used
        - 500 If the server failed to carry out the request
    """

    try:
        data = SignupSchema().load(get_request_body())

        # Not sure how safe this is security wise to tell them exactly what's
        # in use already but i think it would be a UX issue to leave it vague
        if User.query.filter_by(username=data['username']).first() != None:
            return jsonify(error='Username already in use'), 409

        if User.query.filter_by(email=data['email']).first() != None:
            return jsonify(error='Email already in use'), 409

        new_user = User(
            **data, user_type=UserType.query.filter_by(user_type_name='Normal User').first())

        db.session.add(new_user)
        db.session.commit()

        # Generate the JWT Token
        return gen_access_refresh_token(new_user), 200
    except ValidationError as e:
        return jsonify(errors=e.messages), 400


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
        data = SigninSchema().load(get_request_body())

        user: User = User.query.filter_by(username=data['iden']).first(
        ) or User.query.filter_by(email=data['iden']).first()

        if user:
            if user.deleted_at:  # dont sign in deleted users
                return jsonify(
                    error='This user has been deleted'), 401

            if user.check_password(data['password']):
                # Generate the JWT Token
                return gen_access_refresh_token(user), 200

        return jsonify(
            error='Incorrect username or email and password combination'), 401
    except ValidationError as e:
        return jsonify(errors=e.messages), 400


@auth.route('/logout', methods=['POST'])
@token_required
def logout():
    """
    Endpoint for log out

    Returns with message:
        - 200 if successful
        - 400 if the body sent with the request was malformed
        - 500 If the server failed to carry out the request
    """

    payload = get_jwt()

    if not _is_valid_refresh_token(payload):
        return jsonify(error='Token is invalid'), 400

    invalid_t = InvalidToken(
        payload['jti'], datetime.fromtimestamp(payload['exp']))

    db.session.add(invalid_t)
    db.session.commit()

    return jsonify(message='User logged out successfully'), 200


@auth.route('/refresh', methods=['POST'])
@token_required
def refresh():
    """
    Endpoint for refreshing the access token
    """

    payload = get_jwt()

    if not _is_valid_refresh_token(payload):
        return jsonify(error='Token is invalid'), 400

    invalid_t = InvalidToken(
        payload['jti'], datetime.fromtimestamp(payload['exp']))

    db.session.add(invalid_t)
    db.session.commit()

    return gen_access_refresh_token(g.current_user), 200


def _is_valid_refresh_token(payload: dict):
    """
    Validates a Refresh token based on the structure, token blacklist 
    and fingerprint

    Args:
        payload(dict):
            The JWT refresh token payload

    Returns:
        bool -> True if the token is valid, False otherwise
    """

    # check if this token is a refresh token
    if payload.get('type') != 'refresh':
        return False

    # check if this token is already blacklisted
    if InvalidToken.query.get(payload.get('jti')):
        return False

    # check if the fingerprint in the token is the same as the httponly cookie
    # Token sidejacking XSS attack prevention measure
    fingerprint_cookie = request.cookies.get(
        'FuelGuru_Secure_Fgp', default='', type=str)

    if payload.get('fingerprint') != sha256(fingerprint_cookie.encode('utf-8')).hexdigest():
        return False

    # if all checks passed, the token should be valid
    return True


app.register_blueprint(auth, url_prefix='/auth')
