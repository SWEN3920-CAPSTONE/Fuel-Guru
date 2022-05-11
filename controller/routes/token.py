from datetime import datetime, timedelta
from functools import wraps
from uuid import uuid4

import jwt
from config import app
from flask import abort, g, jsonify, make_response, request
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
from model import User
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError


def generate_token(user: User, refresh=False):

    ctime = datetime.utcnow()

    if refresh:
        expiry_time = app.config.get('JWT_REFRESH_LIFESPAN')

        token = jwt.encode({
            'sub': user.id,
            'jti': uuid4().hex,
            'type': 'refresh',
            'iat': ctime,
            'exp': ctime + timedelta(**expiry_time),
        }, app.config.get('SECRET_KEY'), algorithm="HS256")
    else:
        expiry_time = app.config.get('JWT_ACCESS_LIFESPAN')

        token = jwt.encode({
            'sub': user.id,
            'type': 'access',
            'iat': ctime,
            'exp': ctime + timedelta(**expiry_time),
        }, app.config.get('SECRET_KEY'), algorithm="HS256")

    return token


def verify_token(is_admin=False):
    try:
        verify_jwt_in_request()

        data = get_jwt()

        current_user = User.query.get(data.get('sub'))

        if not current_user:
            abort(make_response({"message": "Token is invalid"}, 401))

        if is_admin:
            if current_user.user_type.is_admin != True:
                abort(make_response(
                    {'message', 'The user is not authorized to make this request'}, 403))

    except NoAuthorizationError as e:
        abort(make_response({'message': str(e)}, 401))

    except InvalidSignatureError:
        abort(make_response({"message": 'Token is invalid'}, 401))

    except ExpiredSignatureError:
        abort(make_response({"message": 'Token is expired'}, 401))

    except DecodeError:
        return abort(make_response(
            {'message': 'Token signature is invalid'}, 401))

    g.current_user = current_user


def token_required(f):
    """
    Wraps a functions and makes it token required

    Args:
        f (function):   The function to wrap
    Returns:
        function -> The decorator function
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        verify_token()
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    """
    Wraps a functions and makes it admin required

    Args:
        f (function):   The function to wrap
    Returns:
        function -> The decorator function
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        verify_token(True)
        return f(*args, **kwargs)

    return decorated
