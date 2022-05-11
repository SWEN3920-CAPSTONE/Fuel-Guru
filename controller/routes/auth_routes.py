from datetime import datetime

import jwt
from config import app, csrf, db
from controller.routes.token import admin_required, generate_token, token_required
from controller.validation.schemas import SigninSchema, SignupSchema
from flask import Blueprint, abort, jsonify, make_response, request, g
from marshmallow import ValidationError
from model import User, UserType
from flask_jwt_extended import verify_jwt_in_request, get_jwt

from model.invalid_tokens import InvalidToken

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
        data = SignupSchema().load(request.get_json(
            force=True, silent=True) or request.form.to_dict())

        # Not sure how safe this is security wise to tell them exactly what's
        # in use already but i think it would be a UX issue to leave it vague
        if User.query.filter_by(username=data['username']).first() != None:
            return jsonify({'error': 'Username already in use'}), 409

        if User.query.filter_by(email=data['email']).first() != None:
            return jsonify({'error': 'Email already in use'}), 409

        new_user = User(
            **data, user_type=UserType.query.filter_by(user_type_name='Normal User').first())

        db.session.add(new_user)
        db.session.commit()

        # Generate the JWT Token
        return jsonify({'message': 'User successfully registered', 'access_token': generate_token(new_user),
                        'refresh_token': generate_token(new_user, True)}), 200
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400


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
                # Generate the JWT Token
                return jsonify({
                    'message': 'Login Successful',
                    'access_token': generate_token(user),
                    'refresh_token': generate_token(user, True)
                }), 200

        return jsonify(
            {'error': 'Incorrect username or email and password combination'}), 401
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400


@auth.route('/logout', methods=['POST'])
@csrf.exempt
@token_required
def logout():
    """
    Endpoint for log out

    Returns with message:
        - 200 if successful
        - 400 if the body sent with the request was malformed
        - 500 If the server failed to carry out the request
    """
    verify_jwt_in_request()
    payload = get_jwt()

    if payload['type'] != 'refresh':
        abort(make_response({'error': 'Token is invalid'}, 400))
        
    if InvalidToken.query.get(payload['jti']):
        abort(make_response({'error': 'Token is invalid'}, 400))

    invalid_t = InvalidToken(
        payload['jti'], datetime.fromtimestamp(payload['exp']))

    db.session.add(invalid_t)
    db.session.commit()

    return jsonify({'message': 'User logged out successfully'}), 200


@auth.route('/refresh', methods=['POST'])
@token_required
def refresh():
    """
    Endpoint for refreshing the access token
    """
    verify_jwt_in_request()
    payload = get_jwt()

    if payload['type'] != 'refresh':
        abort(make_response({'error': 'Token is invalid'}, 400))
        
    if InvalidToken.query.get(payload['jti']):
        abort(make_response({'error': 'Token is invalid'}, 400))

    invalid_t = InvalidToken(
        payload['jti'], datetime.fromtimestamp(payload['exp']))

    db.session.add(invalid_t)
    db.session.commit()

    return jsonify({
        'message': 'Login Successful',
        'access_token': generate_token(g.current_user),
        'refresh_token': generate_token(g.current_user, True)
    }), 200


app.register_blueprint(auth, url_prefix='/auth')
