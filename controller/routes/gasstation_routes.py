
from flask import Blueprint
from config import app

gasstation_api = Blueprint('gasstation_api', __name__)

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