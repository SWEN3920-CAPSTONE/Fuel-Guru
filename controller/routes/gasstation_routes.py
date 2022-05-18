
from email import message
from email.mime import image
from pprint import pprint
from flask import Blueprint, jsonify, request
from config import app, db, csrf
from model.gasstation import GasStation
from ..geolocation import init_geolocation
import json

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

@gasstation_api.route('', methods=['POST', 'GET'])
@csrf.exempt
def init_gastations():
    """
    Endpoint is for adding the initial gas station data to the database

    Will run only if the gas station table is empty
    """
    if len(db.session.query(GasStation).all()) == 0 and request.method == 'POST':
        gassations, status = init_geolocation()
        gss = json.loads(gassations.data)['data']
        pprint(json.loads(gassations.data)['data'])
        if status == 200:
            for gasstation in gss:
                name = gasstation.get('name')
                address = gasstation.get('vicinity'),
                lat = gasstation['geometry']['location'].get('lat')
                lng = gasstation['geometry']['location'].get('lng')
                #image = #gasstation.get('icon')
                gs = GasStation(name, address, lat , lng)
                db.session.add(gs)
                db.session.commit()
            return jsonify(message='Gas stations sucessfully added'), 200
        else:
            if status == 404:
                return jsonify(error='No gas stations were found'), 404
            #print(gassations.error)
    else:
        return jsonify(error='gass stations are already in the database')

@gasstation_api.route('/search/nearby', methods=['POST'])
def search_nearby_gasstation():
    """
    Endpoint is for finding the nearest gas stations based on the user's current location.
    """
    #if request.method == 'POST':

    pass

@gasstation_api.route('/find',methods=['POST'])
def find_gasstation():
    """
    Endpoint is for finding a route to a gas station based on the user's current location.
    """
    pass


app.register_blueprint(gasstation_api, url_prefix='/gasstations')