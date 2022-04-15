
from flask import Blueprint
from config import app
from controller.routes.token import admin_required

gasstation_api = Blueprint('gasstation_api', __name__)

@gasstation_api.route('',methods=['POST', 'PUT','DELETE'])
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
        
    Returns with message:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not an admin
        - 500 if there was a server error
    """
    pass

@gasstation_api.route('/search',methods=['POST'])
def search_gasstations():
    """
    Endpoint for handling gas stations search
    
    TBD
        
    Returns with message:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 404 if no gas stations were found
        - 500 if there was a server error
    """
    pass

@gasstation_api.route('/<int:id>', methods=['GET'])
def get_gasstation(id):
    """
    Endpoint for getting gas stations and their associated posts
    
    GET Parms:
        - id (int): gas station id
        
    Returns with message:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 404 If the gas station is malformed
        - 500 if there was a server error
    """
    pass

app.register_blueprint(gasstation_api, url_prefix='/gasstations')