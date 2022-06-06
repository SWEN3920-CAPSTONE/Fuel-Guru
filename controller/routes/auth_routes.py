from datetime import datetime
from hashlib import sha256

import jwt
from config import app, db, mail
from controller.routes.token import gen_jwts, token_required
from controller.utils import (flash_errors, generate_reset_link,
                              get_request_body)
from controller.validation.forms import ResetPassword
from controller.validation.schemas import SigninSchema, SignupSchema
from flask import Blueprint, flash, g, jsonify, render_template, request
from flask_jwt_extended import get_jwt
from flask_mail import Message
from marshmallow import ValidationError
from model.invalid_tokens import InvalidToken
from model.users import User, UserType

auth_api = Blueprint('auth_api', __name__)

# TODO test


@auth_api.route('/signup', methods=['POST'])
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
        return gen_jwts(new_user), 200
    except ValidationError as e:
        return jsonify(errors=e.messages), 400


@auth_api.route('/signin', methods=['POST'])
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
                return gen_jwts(user), 200
        
        return jsonify(
            error='Incorrect username or email and password combination'), 401
    except ValidationError as e:
        return jsonify(errors=e.messages), 400


@auth_api.route('/logout', methods=['POST'])
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


@auth_api.route('/refresh', methods=['POST'])
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

    return gen_jwts(g.current_user,False), 200


@auth_api.route('/forgotpsswd', methods=['POST'])
def forgot_password():
    """
    Sends generated reset link to user email

    Body:
        - email (str):
            The user's email to which the reset link will be sent

    Returns:
        - 200 if successful
        - 401 if no user corresponding to the email exists or has been deleted
        - 500 if something else goes wrong
    """

    data = get_request_body()

    user = User.query.filter_by(email=data.get('email')).first()

    if not user:
        return jsonify(error='User does not exist'), 401

    if user.deleted_at:
        return jsonify(error='This user has been deleted'), 401

    change = generate_reset_link(user)

    ehtml = f"""
    Hi {user.firstname} {user.lastname},
    
    <br>
    <br>We received a request to change your password.
    
    {change}
    """

    msg = Message('Fuel Guru Password Reset Request',
                  recipients=[user.email], html=ehtml)

    mail.send(msg)

    return jsonify(message='Password reset email sent'), 200


@auth_api.route('/resetpsswd/<string:token>', methods=['POST', 'GET'])
def reset_user_password(token):
    """
    Sends generated reset link to user email

    Args:
        token (str):
            The token in the link sent by the forgotpasswd route

    Body:
        - password (str):
            The user's new password

        - conf_password (str):
            The user's new password again

    Returns:
        - 200 if successful
        - 401 if the token is invalid due to malformation or expiry
        - 500 if something else goes wrong
    """
    form = ResetPassword()
    try:
        dtoken = jwt.decode(token, app.config.get(
            'SECRET_KEY'), algorithms=['HS256'])

    except jwt.ExpiredSignatureError as e:
        return jsonify(error='The reset token has expired'), 401

    except:
        return jsonify(error='Something went wrong'), 401

    if InvalidToken.query.get(dtoken.get('jti')):
        return jsonify(error='Invalid reset token'), 401

    user = User.query.get(dtoken.get('sub'))

    if not user:
        return jsonify(error='This user does not exist'), 401

    if user.deleted_at:
        return jsonify(error='This user has been deleted'), 401

    if request.method == 'POST':
        if form.validate_on_submit():
            if form.password.data != form.conf_password.data:
                flash('The passwords do not match', 'error')
            else:
                user.password = form.password.data

                inv_token = InvalidToken(dtoken.get(
                    'jti'), datetime.fromtimestamp(dtoken.get('exp')))

                db.session.add(inv_token)
                db.session.commit()

                return jsonify(message='Password reset success'), 200
        else:
            flash_errors(form)

    return render_template('reset_password.html', form=form, token=token)


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
        # assume attack attempt and black list
        invalid_t = InvalidToken(payload.get(
            'jti'), datetime.fromtimestamp(payload.get('exp')))
        db.session.add(invalid_t)
        db.session.commit()
        return False

    # if all checks passed, the token should be valid
    return True


app.register_blueprint(auth_api, url_prefix='/auth')
