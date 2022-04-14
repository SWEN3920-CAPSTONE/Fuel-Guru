from config import app, db
from controller.routes.token import admin_required, token_required
from flask import abort, g, jsonify, make_response, request
from flask_wtf.csrf import generate_csrf
from model.gasstation import GasStation
from model.posts import (AmenityTag, AmenityType, Comment, Gas,
                         GasPriceSuggestion, GasType, Post, PostType,
                         Promotion, Rating, Review)
from model.users import User, UserType


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
        - post_id (int)
    
    Body for PUT and POST:
        - post_id <PUT only> (int)
        - gas_station_id <POST only> (int)
        - post_type_id <POST only> (int)
        - post_details (one of the following):
            - comment: (dict/object)
                - body (str)
            - rating: (dict/object)
                - rating_val (int)
            - promotion (dict/object):
                - desc (str)
                - start_date (UTC date time stamp)
                - end_date (UTC date & time stamp)
                - [image] (str, optional)
            - review (dict/object):
                - body (str)
                - rating_val (int)         
            - gas_price_suggestion:
                - gases: (each with a)
                    - price
                    - gas_type_id                    
            - amenity_tag:
                - amenity:
                    - amenity_id

    Returns with message:
        - 200 if the request was successful
        - 400 if the request was malformed
        - 401 if the user is not logged in
        - 403 if the user type is not allowed to perform operations on 
        the specified post type
        - 404 if the post requested to be edited is not not found
        - 405 if the user is trying to edit a post after the 30 minute window
        - 500 if the request failed on the server side
    """
    pass

@app.route('/posts/upvote', methods=['POST'])
@token_required
def upvote():
    """
    Endpoint to allow a user to upvote a post
    
    Body:
        - post_id (int)
        
    Returns:
        - 200 if the request was successful
        - 400 if the body was malformed and an error message
        - 401 If the user making the request is not logged in
        - 500 if the request fails and an error message    
    """
    pass

@app.route('/posts/downvote', methods=['POST'])
@token_required
def downvote():
    """
    Endpoint to allow a user to downvote a post
    
    Body:
        - post_id (int)
        
    Returns:
        - 200 if the request was successful
        - 400 if the body was malformed and an error message
        - 401 If the user making the request is not logged in
        - 500 if the request fails and an error message
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
        - post_type_name (str)
    
    Body for PUT:    
        - post_type_name (str)
        - id (int)
        
    Returns:
        - 200 if the request was successful
        - 400 if the request body was malformed for the method 
        and an error message
        - 403 If the user making the request is not an admin
        - 404 if the post type to be edited could not be found
        - 500 if the server fails to carry out the request, and an error message
    """
    pass

@app.route('/auth/signup', methods=['POST'])
def signup():
    """
    Endpoint for signup
    
    Body:
        - username (str)
        - password (str)
        - email (str)
        - firstname (str)
        - lastname (str)
    
    Returns:
        - 201 if successful and a JWT to be stored in the client-side
        - 400 if the body sent with the request was faulty along with 
        an error message
        - 500 If the server failed to carry out the request along with 
        an error message
    """
    pass

@app.route('/auth/signup/manager',methods=['POST'])
@admin_required
def add_gasstation_manager():
    """
    Endpoint for signup
    
    Body:
        - username (str)
        - password (str)
        - email (str)
        - firstname (str)
        - lastname (str)
    
    Returns:
        - 201 if successful and a JWT to be stored in the client-side
        - 400 if the body sent with the request was faulty along with 
        an error message
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not authorized to
        - 500 If the server failed to carry out the request along with 
        an error message
    """
    pass


@app.route('/auth/signin', methods=['POST'])
def signin():
    """
    Endpoint for signin
    
    Body:
        - username or email (str)
        - password (str)
    
    Returns:
        - 200 if successful and a JWT to be stored in the client-side
        - 400 if the body sent with the request was faulty along with 
        an error message
        - 404 if the user + password combo doesnt exist
        - 500 If the server failed to carry out the request along with 
        an error message
    """
    pass


@app.route('/users', methods=['DELETE', 'PUT'])
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
    
    Returns:
        - 200 if the request was successful
        - 400 if the body was empty for PUT or otherwise malformed 
        with error message
        - 401 if the user making the request isnt logged in
        - 500 for server error with error message
    """
    pass


@app.route('/users/types', methods=['POST', 'PUT', 'GET'])
@admin_required
def user_types():
    """
    Endpoint for handling user types
    
    Body for POST:
        - user_type_name
        
    Body for PUT:
        - user_type name
        - id
        
    Returns:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not an admin
        - 500 if there was a server error
    """
    pass

@app.route('/gasstations',methods=['POST', 'PUT','DELETE'])
@admin_required
def gasstations():
    """
    Endpoint for handling gas stations
    
    Body for POST:
        - name
        - address
        - lat
        - lng
        - [image]
        - [manager_id]
        
    Body for PUT:
        - id 
        - (and at least one of the following)
            - name
            - address
            - lat
            - lng
            - image
            - manager_id
        
    Body for DELETE:
        - id
        
    Returns:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not an admin
        - 500 if there was a server error
    """
    pass

@app.route('/gasstations/search',methods=['POST'])
def search_gasstations():
    """
    Endpoint for handling gas stations search
    
    TBD
        
    Returns:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 404 if no gas stations were found
        - 500 if there was a server error
    """
    pass

@app.route('/gasstations/<int:id>', methods=['GET'])
def get_gasstation(id):
    """
    Endpoint for getting gas stations and their associated posts
    
    GET Parms:
        - id (int): gas station id
        
    Returns:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 404 If the gas station is malformed
        - 500 if there was a server error
    """
    pass


@app.route('/amenities/types', methods=['POST', 'PUT','GET'])
@admin_required
def amenity_types():
    """
    Endpoint for handling amenity types
    
    Body for POST:
        - amenity_name
        
    Body for PUT:
        - id 
        - amenity_name
        
    Returns:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not an admin
        - 500 if there was a server error
    """
    pass


@app.route('/gas/types', methods=['POST','PUT','GET'])
@admin_required
def gas_types():
    """
    Endpoint for handling gas types
    
    Body for POST:
        - gas_type_name
        
    Body for PUT:
        - id 
        - gas_type_name
        
    Returns:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not an admin
        - 500 if there was a server error
    """
    pass
