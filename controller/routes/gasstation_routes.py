
from datetime import date, datetime, timedelta

from config import app
from controller.utils import get_request_body
from controller.validation.schemas import GasStationSearchSchema
from flask import Blueprint, jsonify
from marshmallow import ValidationError
from model.gasstation import GasStation
from model.posts import (GasPriceSuggestion, Post, downvoted_posts,
                         upvoted_posts)
from model.schemas import GasStationSchema
from sqlalchemy import and_, desc, func, select
from sqlalchemy.orm import aliased

gasstation_api = Blueprint('gasstation_api', __name__)


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

            today = datetime.fromisoformat(date.today().isoformat())

            yesterday_start = today - timedelta(days=1)

            q = q.join(GasStation.all_posts)\
                .join(GasPriceSuggestion, and_(
                    GasPriceSuggestion.post_id == Post.id,
                    GasPriceSuggestion.last_edited == Post.last_edited))\
                .filter(GasPriceSuggestion.last_edited >= yesterday_start)\
                .join(net, net.c.vid == Post.id).order_by(desc(net.c.net_v))

        if criteria.get('nearest'):
            pass
            # other searches dependent on geolocation

        q = q.limit(5)
        
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


app.register_blueprint(gasstation_api, url_prefix='/gasstations')
