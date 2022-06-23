import json
from datetime import date, datetime, timedelta
from pprint import pprint

from config import app, db
from controller.utils import get_request_body, ja_today
from controller.validation.schemas import (GasStationSearchSchema,
                                           HandleUserLocationSchema)
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from model.gasstation import GasStation
from model.posts import (Gas, GasPriceSuggestion, GasType, Post,
                         downvoted_posts, upvoted_posts)
from model.schemas import GasSchema, GasStationSchema
from sqlalchemy import and_, asc, desc, func, select
from sqlalchemy.orm import aliased

from ..geolocation import init_geolocation, nearby_gasstation

gasstation_api = Blueprint('gasstation_api', __name__)


@gasstation_api.route('', methods=['GET'])
def all_gasstations():
    """
    End point for getting all the gas stations in the system
    
    no body or params
    
    Returns with data:
        - 200 if there are gas stations
        - 404 if there are none        
    """
    stations= GasStation.query.all()
    
    if len(stations)>0:
        return jsonify(data=GasStationSchema(many=True).dump(stations), message='Success'),200
    else:
        return jsonify(data=[], message='No gas stations in the database'),404
    

@gasstation_api.route('/search', methods=['POST'])
def search_gasstations():
    """
    Endpoint for handling gas stations search

    Returns with message:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 404 if no gas stations were found
        - 500 if there was a server error
    """
    try:
        criteria = GasStationSearchSchema().load(get_request_body())

        q = GasStation.query

        if criteria.get('name'):
            q = q.filter(
                GasStation.name.ilike(f'%{criteria.get("name")}%'))
            
        if criteria.get('gas_type_id') or criteria.get('cheapest'):
            q = q.join(GasStation.all_posts)\
                .join(GasPriceSuggestion, and_(
                    GasPriceSuggestion.post_id == Post.id,
                    GasPriceSuggestion.last_edited == Post.last_edited))\
                .join(Gas, Gas.gas_post_id==GasPriceSuggestion.id)
                    
                
        if criteria.get('gas_type_id'):
            q = q.filter(Gas.gas_type_id== criteria.get('gas_type_id'))

        if criteria.get('cheapest'):
            dwn = aliased(
                select(
                    func.count(downvoted_posts.c.posts).label('downvs'),
                    downvoted_posts.c.posts.label('downid'))
                .where(
                    downvoted_posts.c.posts == Post.id)
                .group_by(downvoted_posts.c.posts).subquery(), name='downvote_count')

            upv = aliased(
                select(
                    func.count(upvoted_posts.c.posts).label('upvs'),
                    upvoted_posts.c.posts.label('upid'))
                .where(upvoted_posts.c.posts == Post.id)
                .group_by(upvoted_posts.c.posts).subquery(), name='upvote_count')

            net = aliased(select(
                (func.coalesce(upv.c.upvs, 0) -
                 func.coalesce(dwn.c.downvs, 0)).label('net_v'),
                upv.c.upid.label('vid'))
                .select_from(
                dwn.join(upv, dwn.c.downid == upv.c.upid, full=True)).subquery(), name='net_votes')

            today = ja_today()

            yesterday_start = today - timedelta(days=1)
            
            q=q.filter(GasPriceSuggestion.last_edited >= yesterday_start)\
                .join(net, net.c.vid == Post.id).order_by(desc(net.c.net_v)).order_by(asc(Gas.price))

        if criteria.get('nearest'):
            pass
            # other searches dependent on geolocation


        
        res = GasStationSchema(many=True).dump(q.all())

        if len(res) > 0:
            return jsonify(message='Search successful', data=res), 200
        else:
            return jsonify(message='No gas stations found', data=res), 404

    except ValidationError as e:
        return jsonify(errors=e.messages), 400


# filter by date
@gasstation_api.route('/<int:station_id>', methods=['GET'])
def get_gasstation(station_id):
    """
    Endpoint for getting gas stations and their associated posts

    GET Parms:
        - id (int): gas station id

    Returns with message:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 404 If the gas station is not found
        - 500 if there was a server error
    """
    gasstation = GasStation.query.get(station_id)

    if not gasstation:
        return jsonify(error='The specified gasstation does not exist'), 404

    data = GasStationSchema().dump(gasstation)

    return jsonify(message='Fetch was successful', data=data), 200


@gasstation_api.route('/search/nearby', methods=['POST'])
def search_nearby_gasstation():
    """
    Endpoint is for finding the nearest gas stations based on the user's current location.
    """
    try:
        if request.method == 'POST':
            data : dict = HandleUserLocationSchema().load(get_request_body())
            res, status = nearby_gasstation(data.get('lat'), data.get('lng'))
            if status == 200:
                resdata = json.loads(res.data)['data']
                return jsonify(message='Nearby Gasstations retrived successfully', data=resdata), 200
            else:
                if status == 404:
                    return jsonify(error='You are not nearby any gas stations'), 404
                return jsonify(error="Something went wrong on the server's side, please try again later"), 500
        else:
            return jsonify(error='Method not allowed'), 405
    except ValidationError as e:
        return jsonify(errors=e.messages), 400
    
        
@gasstation_api.route('/top',methods=['GET'])
def top_gasstations():
    """
    Find the lowest gas prices by gas type for yesterday and today
    """
    today = ja_today()
    
    dwn = aliased(
            select(
                func.count(downvoted_posts.c.posts).label('downvs'),
                downvoted_posts.c.posts.label('downid'))
            .where(
                downvoted_posts.c.posts == Post.id)
            .group_by(downvoted_posts.c.posts).subquery(), name='downvote_count')

    upv = aliased(
        select(
            func.count(upvoted_posts.c.posts).label('upvs'),
            upvoted_posts.c.posts.label('upid'))
        .where(upvoted_posts.c.posts == Post.id)
        .group_by(upvoted_posts.c.posts).subquery(), name='upvote_count')

    net = aliased(select(
        (func.coalesce(upv.c.upvs, 0) -
            func.coalesce(dwn.c.downvs, 0)).label('net_v'),
        upv.c.upid.label('vid'))
        .select_from(
        dwn.join(upv, dwn.c.downid == upv.c.upid, full=True)).subquery(), name='net_votes')
    
    gas_types = GasType.query.all()
    res = []
    for gtype in gas_types:
        gas= Gas.query.filter(Gas.gas_type_id==gtype.id)\
            .from_self(Gas)\
            .join(GasPriceSuggestion, GasPriceSuggestion.id==Gas.gas_post_id)\
            .join(GasPriceSuggestion.post)\
            .filter(Post.last_edited>=today)\
            .join(net, net.c.vid == Post.id, full=True)\
            .filter(net.c.net_v >=0)\
            .order_by(desc(net.c.net_v))\
            .order_by(desc(Post.last_edited))\
            .order_by(asc(Gas.price))\
            .limit(1)\
            .first()
        
        if gas:
            res.append(GasSchema().dump(gas))
    
    if len(res) >0:
        return jsonify(data=res, message='Success'),200
    else:
        return jsonify(message='Nothing found'),404
        
app.register_blueprint(gasstation_api, url_prefix='/gasstations')


def init_gastations():
    """
    Endpoint is for adding the initial gas station data to the database

    Will run only if the gas station table is empty
    """
    if len(db.session.query(GasStation).all()) == 0:
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
