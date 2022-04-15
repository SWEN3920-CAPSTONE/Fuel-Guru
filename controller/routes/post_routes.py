from flask import Blueprint
from controller.routes.token import admin_required, token_required
from config import app

posts_api = Blueprint('posts_api', __name__)

@posts_api.route('', methods=['POST','DELETE','PUT'])
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
        - 403 if the user type is not allowed to perform CRUD operations 
        on the specified post type
        - 404 if the post requested to be edited is not not found
        - 405 if the user is trying to edit a post after the 30 minute window
        - 500 if the request failed on the server side
    """
    pass

@posts_api.route('/upvote', methods=['POST'])
@token_required
def upvote():
    """
    Endpoint to allow a user to upvote a post
    
    Body:
        - post_id (int)
        
    Returns with message:
        - 200 if the request was successful
        - 400 if the body was malformed
        - 401 If the user making the request is not logged in
        - 403 If the user's type is not allowed to upvote
        - 404 If the post does not exist
        - 500 if the request fails on the server's part    
    """
    pass

@posts_api.route('/downvote', methods=['POST'])
@token_required
def downvote():
    """
    Endpoint to allow a user to downvote a post
    
    Body:
        - post_id (int)
        
    Returns with message:
        - 200 if the request was successful
        - 400 if the body was malformed
        - 401 If the user making the request is not logged in
        - 403 If the user's type is not allowed to downvote
        - 404 If the post does not exist
        - 500 if the request fails
    """
    pass

@posts_api.route('/types', methods=['POST', 'PUT', 'GET'])
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
        
    Returns with message:
        - 200 if the request was successful
        - 400 if the request body was malformed for the method
        - 403 If the user making the request is not an admin
        - 404 if the post type to be edited could not be found
        - 500 if the server fails to carry out the request
    """
    pass

app.register_blueprint(posts_api, url_prefix='/posts')