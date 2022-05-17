from datetime import datetime, timedelta
from functools import wraps
from hashlib import sha256
from uuid import uuid4

import jwt
from config import app
from flask import abort, g, make_response
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
from model.users import User


def gen_access_refresh_token(user: User):
    """
    Generates a new JWT access and refresh token for a given user

    Args:
        user(User):
            The user the tokens should be generated for

    Returns:
        Response(partial) -> Response containing the tokens
    """

    ctime = datetime.utcnow()

    # create fingerprint cookie contents
    fingerprint = str(uuid4())

    # create refresh token
    rtoken = jwt.encode({
        'sub': user.id,
        'jti': uuid4().hex,
        'type': 'refresh',
        # hash fingerprint
        'fingerprint': sha256(fingerprint.encode('utf-8')).hexdigest(),
        'iat': ctime,
        'exp': ctime + timedelta(**app.config.get('JWT_REFRESH_LIFESPAN')),
    }, app.config.get('SECRET_KEY'), algorithm="HS256")

    # create access token
    atoken = jwt.encode({
        'sub': user.id,
        'type': 'access',
        'iat': ctime,
        'exp': ctime + timedelta(**app.config.get('JWT_ACCESS_LIFESPAN')),
    }, app.config.get('SECRET_KEY'), algorithm="HS256")

    res = make_response(
        {'access_token': atoken, 'refresh_token': rtoken, 'message': 'Success'})

    # set fingerprint cookie
    res.set_cookie('FuelGuru_Secure_Fgp', fingerprint,
                   max_age=timedelta(**app.config.get('JWT_REFRESH_LIFESPAN')),
                   expires=(
                       ctime + timedelta(**app.config.get('JWT_REFRESH_LIFESPAN'))),
                   httponly=True,
                   secure=not app.config.get('IS_DEV'),
                   samesite='Strict')

    return res


def _verify_token(is_admin=False):
    try:
        # get JWT from request
        verify_jwt_in_request()

        data = get_jwt()

        # get user from JWT
        current_user: User = User.query.get(data.get('sub'))

        # dont authenticate if the token doesnt correspond to a real user
        if not current_user:
            abort(make_response({"error": "Token is invalid"}, 401))

        # dont authenticate if the corresponding user has been deleted
        if current_user.deleted_at:
            abort(make_response({"error": "This user has been deleted"}, 401))

        # dont authenticate if the route requires admin privledges
        # but the user does not have admin
        if is_admin:
            if current_user.user_type.is_admin != True:
                abort(make_response(
                    {'error', 'The user is not authorized to make this request'}, 403))

    except NoAuthorizationError as e:
        abort(make_response({'error': str(e)}, 401))

    except InvalidSignatureError:
        abort(make_response({"error": 'Token is invalid'}, 401))

    except ExpiredSignatureError:
        abort(make_response({"error": 'Token is expired'}, 401))

    except DecodeError:
        return abort(make_response(
            {'error': 'Token signature is invalid'}, 401))

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
        _verify_token()
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
        _verify_token(True)
        return f(*args, **kwargs)

    return decorated
