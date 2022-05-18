from pprint import pprint
from urllib import response
from flask import jsonify
from config import app
import requests

API_KEY = app.config.get('API_KEY')
'''api_key.txt is git ignored, request API key from owner if necessary'''

#This URL requests nearby gas stations
url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'

#This is URL requests directions from the user's current location to the destination
url_route = 'https://maps.googleapis.com/maps/api/directions/json?'


def init_geolocation():
    try:
        #10 Gas Stations 1500 meters from the coodinates 18.024960, -76.796557 (New Kingston Area)
        res_init = requests.get(url + 'location=18.024960%2C-76.796557' + '&radius=1500' + '&type=gas_station' + '&key=' + API_KEY)
        if res_init.json()['status'] == 'OK':
            return jsonify(message=res_init.json()['status'], data=res_init.json()['results']), 200

        elif res_init.json()['status'] == 'ZERO_RESULTS':
            return jsonify(error=res_init.json()['status'], data='{}'), 404

        elif res_init.json()['status'] == 'INVALID_REQUEST':
            return jsonify(error=res_init.json()['status'], data='{}'), 400

        elif res_init.json()['status'] == 'REQUEST_DENIED':
            return jsonify(error=res_init.json()['status'], data='{}'), 500        
    except:
        return jsonify(error='An unknown error occured', data='{}')

def nearby_gasstation(lat, lng):    
#Gas Stations relative to user's currect location
    user_location = {'lat' : lat, 'lng': lng } #This should be where the user's location is provided
    #Contains gas stations nearby relative to the current user's location
    try:
        res_current = requests.get(url + 'location=' + user_location.get('lat') +'%2C'+ user_location.get('lng') + '&radius=1500' + '&type=gas_station' + '&key=' + API_KEY)
        if res_current.json()['status'] == 'OK':
            return jsonify(message=res_current.json()['status'], data=res_current.json()['results']), 200
        elif res_current.json()['status'] == 'ZERO_RESULTS':
            return jsonify(error=res_current.json()['status'], data='{}'), 404

        elif res_current.json()['status'] == 'INVALID_REQUEST':
            return jsonify(error=res_current.json()['status'], data='{}'), 400

        elif res_current.json()['status'] == 'REQUEST_DENIED':
            return jsonify(error=res_current.json()['status'], data='{}'), 500   
    except:
        return jsonify(error='An unknown error occured', data='{}')

def nearby_gasstation(mylat, mylng, lat, lng):
    user_location = {'lat' : mylat, 'lng': mylng } #This should be where the user's location is provided    
    des_location = {'lat' : lat, 'lng': lng} #This should be where the destination's location is provided
    try:
        res_route = requests.get(url_route + 'origin=' + user_location.get('lat') +'%2C'+ user_location.get('lng') +'&destination=' + des_location.get('lat') + '%2C' + des_location.get('lat') + '&key=' + API_KEY)
        if res_route.json()['status'] == 'OK':
            return jsonify(message=res_route.json()['status'], data=res_route.json()['results']), 200
        elif res_route.json()['status'] == 'ZERO_RESULTS' or res_route.json()['status'] == 'NOT_FOUND':
            return jsonify(error=res_route.json()['status'], data='{}'), 404
        elif res_route.json()['status'] == 'INVALID_REQUEST':
            return jsonify(error=res_route.json()['status'], data='{}'), 400
        elif res_route.json()['status'] == 'REQUEST_DENIED':
            return jsonify(error=res_route.json()['status'], data='{}'), 500  
    except:
        return jsonify(error='An unknown error occured', data='{}')

#pprint(res_init.json())

