from datetime import date, datetime, timedelta
from pprint import pprint

from config import app, db
from controller.routes.token import token_required
from controller.utils import get_request_body, utc_today
from controller.validation.schemas import HandlePostSchema, PostVoteSchema
from flask import Blueprint, g, jsonify, request
from marshmallow import ValidationError
from model.gasstation import GasStation
from model.posts import (AmenityTag, AmenityType, Gas,
                         GasPriceSuggestion, GasType, Post, PostType,
                         Promotion, Review)
from model.schemas import (AmenityTagSchema, AmenityTypeSchema,
                           GasPriceSuggestionSchema, GasTypeSchema, PostSchema,
                           PostTypeSchema, PromotionSchema, ReviewSchema)
from sqlalchemy import and_, func
from sqlalchemy.exc import SQLAlchemyError

posts_api = Blueprint('posts_api', __name__)

def _handle_gas_price_suggestion_post(data,post,is_edit):
    details = data.get('gas_price_suggestion')
    if not details:
        return jsonify(error='Gas price suggestion missing or malformed'), 400

    gas_post = GasPriceSuggestion(post, edit=is_edit)

    gases = []
    existing = []
    today = utc_today()
    
    for gas in details.get('gases'):
        gas_type = GasType.query.get(gas.get('gas_type_id'))
        if not gas_type:
            return jsonify(error='A specified gas type does not exist'), 400
        
        gas_obj =Gas(gas.get('price'), gas_type, gas_post)
        gases.append(gas_obj)

    req_prices=[g.price for g in gases]
    req_gtype_ids =[g.gas_type.id for g in gases]
    
    if len(set(req_gtype_ids)) != len(req_gtype_ids):
        return jsonify(error='Only one price per gas type allowed per post'),400
    
    q=Post.query.filter(Post.gas_station_id == post.gas_station_id)\
        .from_self(func.array_agg(Gas.gas_type_id), func.array_agg(Gas.price), Post)\
            .join(GasPriceSuggestion, and_(
                GasPriceSuggestion.post_id == Post.id,
                GasPriceSuggestion.last_edited == Post.last_edited))\
            .filter(GasPriceSuggestion.last_edited >= today)\
            .join(GasPriceSuggestion.gases)\
            .filter(Gas.price.in_(req_prices)).filter(Gas.gas_type_id.in_(req_gtype_ids)).group_by(Post)

    existing = q.all()

    if existing:
        
        for epost in existing:
            if ((sorted(epost[0]) == sorted(req_gtype_ids)) and (sorted(epost[1]) == sorted(req_prices))):                    
                
                if post.creator.user_type.can_vote:
                    if post.creator == epost[2].creator:
                        return jsonify(error='You already made this post today'),400
                    
                    if post.creator in epost[2].upvoters:
                        return jsonify(error='These prices have already been posted today and the user has already upvoted that post'), 400
                    
                    if post.creator in epost[2].downvoters:
                        epost[2].downvoters.remove(post.creator)
                        
                    epost[2].upvoters.append(post.creator)

                    db.session.commit()

                    return jsonify(message='These prices have already been posted so those prices have been upvoted instead'), 202
                else:
                    return jsonify(error='These prices have already been posted'), 400
    
    db.session.add(gas_post)
    db.session.add_all(gases)
    db.session.commit()

    if is_edit:
        msg = 'The gas price suggestion has been updated successfully'
    else:
        msg = 'Gas Price Suggestion created successfully'
        
    return jsonify(data=GasPriceSuggestionSchema().dump(gas_post), message=msg),200

def _handle_promotion_post(data,post,is_edit):
    details = data.get('promotion')
    
    if not details:
        return jsonify(error='Promotion missing or malformed'), 400

    if details.get('end_date') < details.get('start_date'):
        return jsonify(error='The end date cannot be earlier than the start date'), 400
        
    promo = Promotion(post=post, **details, edit=is_edit)
    db.session.add(promo)
    db.session.commit()
    
    if is_edit:
        msg = 'The promotion tag has been updated successfully'
    else:
        msg = 'Promotion created successfully'

    return jsonify(data=PromotionSchema().dump(promo), message=msg)
    
def _handle_amenity_post(data,post,is_edit):
    details = data.get('amenity_tag')
    
    if not details:
        return jsonify(error='Amenity id missing or malformed'), 400

    amenity_type = AmenityType.query.get(details.get('amenity_id'))
    
    if not amenity_type:
        return jsonify(error='The specified amenity type does not exist'), 400

    amenity_tag = AmenityTag(amenity_type, post, edit=is_edit)

    q = Post.query.filter(Post.gas_station_id == post.gas_station_id)\
        .join(AmenityTag, and_(
            AmenityTag.post_id == Post.id,
            AmenityTag.last_edited == Post.last_edited))\
        .filter(AmenityTag.amenity_type_id == amenity_type.id)
    
    existing = q.first()

    if existing:
        if post.creator.user_type.can_vote:
            if post.creator == existing.creator:
                return jsonify(error='You already made this post today'),400
                    
            if post.creator in existing.upvoters:
                return jsonify(error='This amenity has already been posted today and the user has already upvoted that post'), 400
            else:
                if post.creator in existing.downvoters:
                    existing.downvoters.remove(post.creator)
                    
                existing.upvoters.append(post.creator)

                db.session.commit()

                return jsonify(message='This amenity has already been posted so that amenity has been upvoted instead'), 202
        else:
            return jsonify(error='This amenity has already been posted'), 400
    else:
        db.session.add(amenity_tag)
        db.session.commit()

    if is_edit:
        msg = 'The amenity tag has been updated successfully'
    else:
        msg ='Amenity created successfully'
        
    return jsonify(data=AmenityTagSchema().dump(amenity_tag), message=msg),200
    
def _handle_review_post(data,post,is_edit):
    details = data.get('review')
    if not details:
        return jsonify(error='Review missing or malformed'), 400

    rev = Review(post=post,body=details.get('body'),rating_val=details.get('rating_val'), edit=is_edit)
    
    db.session.add(rev)
    db.session.commit()

    if is_edit:
        msg = 'The review has been updated successfully'
    else:
        msg ='Review created successfully'
        
    return jsonify(data=ReviewSchema().dump(rev),message=msg),200

def _manage_post_by_type(data: dict, post: Post, is_edit=False):
    """
    Create or edit a post and its details

    Args:            
        data (dict):
            The data to be used to edit or create the post

        post (Post):
            The new post to be adde to the database or the existing post to be edited

        is_edit (bool):
            True if an existing post should be edited or False if a new post should be created

    Returns:
        dict -> The serialized post    
    """

    if post.post_type.post_type_name == 'Review':
        return _handle_review_post(data,post,is_edit)

    if post.post_type.post_type_name == 'Amenity Tag':
        return _handle_amenity_post(data,post,is_edit)

    if post.post_type.post_type_name == 'Promotion':
        return _handle_promotion_post(data,post,is_edit)

    if post.post_type.post_type_name == 'Gas Price Suggestion':
        return _handle_gas_price_suggestion_post(data,post,is_edit)


@posts_api.route('', methods=['POST', 'DELETE', 'PUT'])
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
        - 404 if the post requested to be edited is not found or deleted
        - 405 if the user is trying to edit a post after the 30 minute window
        - 500 if the request failed on the server side
    """
    try:
        if request.method == 'POST':
            data = HandlePostSchema(context={'method': request.method}, exclude=(
                'post_id',)).load(get_request_body())

            post_type: PostType = PostType.query.get(data.get('post_type_id'))

            if not (post_type in g.current_user.user_type.allowed_post_types):
                return jsonify(error=f'This user is not allowed to make {post_type.post_type_name} posts'), 403

            gas_station: GasStation = GasStation.query.get(
                data.get('gas_station_id'))
            
            if not gas_station:
                return jsonify(error='The specified gas station does not exist'),404
            
            if g.current_user.user_type.user_type_name =='Gas Station Manager' and gas_station.manager !=g.current_user:
                return jsonify(error='Gas station managers can only make posts for gas stations they manage'), 403

            post = Post(gas_station, post_type, g.current_user)

            return _manage_post_by_type(data, post, False)
        
        if request.method == 'PUT':
            data = HandlePostSchema(context={'method': request.method}, exclude=(
                'gas_station_id', 'post_type_id')).load(get_request_body())

            post: Post = Post.query.get(data.get('post_id'))

            if not post:
                return jsonify(error='The specified post does not exist'), 404

            if post.deleted_at:
                return jsonify(error='The specified post has been deleted'), 404

            if post.creator != g.current_user:
                return jsonify(error='Only the owner of the specified post may edit it. You are not the owner'), 403
            
            if (post.created_at + timedelta(minutes=30)) < datetime.utcnow():
                return jsonify(error='The 30-minute modification window has passed for the specified post'), 405

            return _manage_post_by_type(data, post, True)

        if request.method == 'DELETE':
            data = HandlePostSchema(context={'method': request.method}, only=(
                'post_id',)).load(get_request_body())

            post: Post = Post.query.get(data.get('post_id'))

            if not post:
                return jsonify(error='The specified post does not exist'), 404

            if post.deleted_at:
                return jsonify(error='The specified post has been deleted already'), 404

            if post.creator != g.current_user:
                return jsonify(error='Only the owner of the specified post may delete it. You are not the owner'), 403
            
            if (post.created_at + timedelta(minutes=30)) < datetime.utcnow():
                return jsonify(error='The 30-minute modification window has passed for the specified post'), 405
            

            post.deleted_at = datetime.utcnow()
            db.session.commit()

            return jsonify(message='The post was successfully deleted'), 200

        else:
            return jsonify(error='method not allowed'), 405

    except ValidationError as e:
        print(e.messages)
        return jsonify(errors=e.messages), 400


def _vote_on_post(success_msg, focus_attr, other_attr):
    """
    Toggles a vote on a post by a user

    Args:
        success_msg (str):
            returned when the toggle was successful

        focus_attr (str):
            The name of the attribute that should be toggled

        other_attr (str):
            The name of the attribute that needs to checked for logical violations

    Returns:
        Response -> 
    """

    if not g.current_user.user_type.can_vote:
        return jsonify(error='This user is not allowed to vote on posts'), 403

    try:
        data = PostVoteSchema().load(get_request_body())

        post: Post = Post.query.get(data.get('post_id'))

        if post:
            if post.deleted_at:
                return jsonify(error='The specified post has been deleted'), 404

            if not post.post_type.is_votable:
                return jsonify(error='The type of the specified post is not votable'), 405
            
            if post.creator == g.current_user:
                return jsonify(error='Users cannot vote on their own posts'),403

            # toggle vote
            if g.current_user in getattr(post, other_attr):
                other = getattr(post, other_attr)
                other.remove(g.current_user)
                setattr(post, other_attr, other)

            if g.current_user in getattr(post, focus_attr):
                focus = getattr(post, focus_attr)
                focus.remove(g.current_user)
                setattr(post, focus_attr, focus)
            else:
                setattr(post, focus_attr, getattr(
                    post, focus_attr) + [g.current_user])

            # just to be safe
            if g.current_user in post.downvoters and g.current_user in post.upvoters:
                raise SQLAlchemyError(
                    'A user cannot both upvote and downvote the same post simultaneously')

            db.session.commit()

            return jsonify(message=success_msg, data=PostSchema().dump(post)), 200
        else:
            return jsonify(error='The specified post does not exist'), 404
    except ValidationError as e:
        return jsonify(errors=e.messages), 400


@posts_api.route('/upvote', methods=['POST'])
@token_required
def upvote():
    """
    Endpoint to allow a user to toggle upvote on a post

    Body:
        - post_id (int)

    Returns with message:
        - 200 if the request was successful
        - 400 if the body was malformed
        - 401 If the user making the request is not logged in
        - 403 If the user's type is not allowed to upvote or if the user 
        is trying to upvote their own post
        - 404 If the post does not exist or has been deleted
        - 405 if the post type is not votable
        - 500 if the request fails on the server's part    
    """
    return _vote_on_post('Upvote toggled successfully', 'upvoters', 'downvoters')


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
        - 405 if the post type is not votable
        - 500 if the request fails
    """
    return _vote_on_post('Downvote toggled successfully', 'downvoters', 'upvoters')


@posts_api.route('/amenities/types', methods=['GET'])
@token_required
def get_amenity_types():
    """
    Fetches all the amenity types in the database
    """
    data = AmenityTypeSchema(many=True).dump(AmenityType.query.all())
    return jsonify(message='Fetch successful', data=data)


@posts_api.route('/gas/types', methods=['GET'])
@token_required
def gas_types():
    """
    Fetches all the gas types in the database
    """
    data = GasTypeSchema(many=True).dump(GasType.query.all())
    return jsonify(message='Fetch successful', data=data)


@posts_api.route('/types', methods=['GET'])
@token_required
def get_post_types():
    """
    Fetches all post types that is user is allowed to make
    """
    data = g.current_user.user_type.allowed_post_types
    data = PostTypeSchema(many=True).dump(data)
    return jsonify(message='Fetch successful', data=data)


app.register_blueprint(posts_api, url_prefix='/posts')
