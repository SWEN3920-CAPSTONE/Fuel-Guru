from functools import wraps

import jwt
from config import app
from flask import abort, g, jsonify, make_response, request
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
from model.users import User


def find_token():
    auth = request.headers.get('Authorization', None)

    if not auth:
        return jsonify(
            {'message': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        return jsonify(
            {'message': 'Authorization header must start with Bearer'}
        ), 401

    elif len(parts) == 1:
        return jsonify({'message': 'Token not found'}), 401

    elif len(parts) > 2:
        return jsonify(
            {'message': 'Authorization header must be Bearer + \s + token'}
        ), 401

    token = parts[1]
    return token
        
        
def verify_token(token, is_admin=False):
    try:
        data = jwt.decode(token, app.config.get(
            'SECRET_KEY'), algorithms="HS256")

        # may be changed when auth is complete
        current_user = User.query.get(data.get('id'))

        if not current_user:
            abort(make_response({"message": "Token is invalid, no user matched to token"}, 401))
        
        if is_admin:
            if current_user.user_type.is_admin != True:
                abort(make_response({'message', 'The user is not authorized to make this request'},403))

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
        verify_token(find_token())
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
        verify_token(find_token(),True)
        return f(*args, **kwargs)

    return decorated
