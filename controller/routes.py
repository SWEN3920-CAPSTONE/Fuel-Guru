from functools import wraps
from flask import abort, jsonify, make_response, g
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
import jwt
from config import app, db
from model.gasstation import GasStation
from model.posts import (PostType, Post, AmenityTag, AmenityType,
                         Comment, Gas, GasPriceSuggestion, GasType, Promotion, Rating, Review)
from model.users import User, UserType
from flask_wtf.csrf import generate_csrf
from flask import request


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

        # or request.cookies.get('token', None)
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

        try:
            data = jwt.decode(token, app.config.get(
                'SECRET_KEY'), algorithms="HS256")

            # may be changed when auth is complete
            current_user = User.query.get(data.get('id'))

            if not current_user:
                abort(make_response({"message": "Token is invalid, no user matched to token"}, 401))

        except InvalidSignatureError:
            abort(make_response({"message": 'Token is invalid'}, 401))

        except ExpiredSignatureError:
            abort(make_response({"message": 'Token is expired'}, 401))

        except DecodeError:
            return abort(make_response(
                {'message': 'Token signature is invalid'}, 401))

        g.current_user = current_user
        return f(*args, **kwargs)

    return decorated

def admin_required(f):
    """
    Wraps a functions and makes it token required
    Args:
        f (function):   The function to wrap
    Returns:
        function -> The decorator function
    """

    @wraps(f)
    def decorated(*args, **kwargs):

        # or request.cookies.get('token', None)
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

        try:
            data = jwt.decode(token, app.config.get(
                'SECRET_KEY'), algorithms="HS256")

            # may be changed when auth is complete
            current_user = User.query.get(data.get('id'))

            if not current_user:
                abort(make_response({"message": "Token is invalid, no user matched to token"}, 401))
            
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
        return f(*args, **kwargs)

    return decorated
        
            
@app.after_request
def setheaders(resp):
    if resp ==None:
        resp = make_response()
    resp.set_cookie('CSRF-TOKEN', generate_csrf()) # to protect form submissions
    

@app.route('/posts', methods=['POST','DELETE','PUT'])
@token_required
def posts():
    """
    Endpoint for handling most post operations
    
    If method == POST:
        Creates a post based on the information sent
    If method == DELETE:
        Deletes a post based on the information sent
    If method == PUT:
        Updates a post based on the information sent
        
    Body for DELETE:
        post_id
    
    Body for PUT and POST:
        post_id (PUT only)
        
        gas_station_id
        
        post_type_id
        
        post_details (one of the following):
            
            comment:
                body
            rating:
                rating_val
            promotion:
                desc
                
                start_date
                
                end_date
                
                image
            review:
                body
                
                rating_val                
            gas_price_suggestion:
                gases: (each with a)
                    price
                    
                    gas_type_id                    
            amenity_tag:
                amenity:
                    amenity_id

    Returns:
        200 if the request was successful
        
        400 if the request was malformed and an error message
        
        401 if the user is not logged in
        
        403 if the user type is not allowed to perform operations on 
        the specified post type
        
        500 if the request failed and an error message
    """
    pass

@app.route('/posts/upvote', methods=['POST'])
@token_required
def upvote():
    """
    Endpoint to allow a user to upvote a post
    
    Body:
        post_id
        
    Returns:
        200 if the request was successful
        
        400 if the body was malformed and an error message
        
        401 If the user making the request is not logged in
        
        500 if the request fails and an error message    
    """
    pass

@app.route('/posts/downvote', methods=['POST'])
@token_required
def downvote():
    """
    Endpoint to allow a user to downvote a post
    
    Body:
        post_id
        
    Returns:
        200 if the request was successful
        
        400 if the body was malformed and an error message
        
        401 If the user making the request is not logged in
        
        500 if the request fails and an error message
    """
    pass

@app.route('/posts/types', methods=['POST', 'PUT', 'GET'])
@admin_required
def post_types():
    """
    Endpoint for handling all post type operations
    
    If method == POST:
        Creates a post type based on the information sent
    If method == GET:
        Gets all post types
    If method == PUT:
        Updates a post type based on the information sent
        
    Body for POST: 
        post_type_name
    
    Body for PUT:    
        post_type_name
        
        id (for existing post type)
        
    Returns:
        200 if the request was successful
        
        400 if the request body was malformed for the method and an error message
        
        403 If the user making the request is not an admin
        
        500 if the server fails to carry out the request, and an error message
    """
    pass


@app.route('/auth/signup', methods=['POST'])
def signup():
    """
    Endpoint for signup
    
    Body:
        username
        
        password
        
        email
        
        firstname
        
        lastname
        
        user_type
    
    Returns:
        201 if successful and a JWT to be stored in the client-side
        
        400 if the body sent with the request was faulty along with an error message
        
        500 If the server failed to carry out the request along with an error message
    """
    pass


@app.route('/auth/signin', methods=['POST'])
def signin():
    """
    Endpoint for signin
    
    Body:
        username or email
        
        password
    
    Returns:
        200 if successful and a JWT to be stored in the client-side
        
        400 if the body sent with the request was faulty along with an error message
        
        404 if the user + password combo doesnt exist
        
        500 If the server failed to carry out the request along with an error message
    """
    pass


@app.route('/users', methods=['DELETE', 'PUT'])
@token_required
def edit_user():
    """
    Endpoint for editing or deleting a user
    
    No body for DELETE
    
    Body for PUT (one of the following):
        [firstname]
        
        [lastname]
        
        [email]
        
        [password]
    
    Returns:
        200 if the request was successful
        
        400 if the body was empty for PUT or otherwise malformed 
        with error message
        
        401 if the user making the request isnt logged in
        
        500 for server error with error message
    """
    pass


@app.route('/users/types', methods=['POST', 'PUT', 'GET'])
@admin_required
def user_types():
    """
    """
    pass

@app.route('/gasstations',methods=['POST', 'PUT','DELETE'])
@admin_required
def gasstations():
    """
    """
    pass

@app.route('/gasstations/search',methods=['POST'])
def search_gasstations():
    """
    """
    pass

@app.route('/gasstations/<int:id>', methods=['GET'])
def get_gasstation(id):
    """
    """
    pass

@app.route('/amenities/types', methods=['POST', 'PUT','GET'])
@admin_required
def amenity_types():
    """
    """
    pass


@app.route('/gas/types', methods=['POST','PUT','GET'])
@admin_required
def gas_types():
    """
    """
    pass
