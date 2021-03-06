import requests
from config import app
from flask import jsonify

API_KEY = app.config.get('API_KEY')

#This URL requests nearby gas stations
url = app.config.get('URL')

#This is URL requests directions from the user's current location to the destination
url_route = app.config.get('URL_ROUTE')


def init_geolocation():
    try:
        #10 Gas Stations 1500 meters from the coodinates 18.024960, -76.796557 (New Kingston Area)
        res_init = requests.get(url + 'location=18.024960%2C-76.796557' + '&radius=5000' + '&type=gas_station' + '&key=' + API_KEY)
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
    #Contains gas stations nearby relative to the current user's location
    try:
        res_current = requests.get(url + 'location=' + str(lat) +'%2C'+ str(lng) + '&radius=5000' + '&type=gas_station' + '&key=' + API_KEY)
        if res_current.json()['status'] == 'OK':
            return jsonify(message=res_current.json()['status'], data=res_current.json()['results']), 200
        elif res_current.json()['status'] == 'ZERO_RESULTS':
            return jsonify(error=res_current.json()['status'], data='{}'), 404

        elif res_current.json()['status'] == 'INVALID_REQUEST':
            return jsonify(error=res_current.json()['status'], data='{}'), 400

        elif res_current.json()['status'] == 'REQUEST_DENIED':
            return jsonify(error=res_current.json()['status'], data='{}'), 500   
    except:
        return jsonify(error='An unknown error occured', data='{}'), 500


