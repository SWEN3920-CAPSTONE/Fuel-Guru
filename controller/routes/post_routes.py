from datetime import datetime, timedelta
from config import app, db
from controller.routes.token import admin_required, token_required
from controller.validation.schemas import HandlePostSchema, HandlePostTypesSchema, PostVoteSchema
from flask import Blueprint, g, jsonify, request
from marshmallow import ValidationError
from model import Post, GasStation, PostType, Comment, Review, Rating, GasPriceSuggestion, AmenityTag, AmenityType, GasType, Gas, Promotion
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from model.schemas import AmenityTagSchema, CommentSchema, GasPriceSuggestionSchema, PostSchema, PostTypeSchema, PromotionSchema, ReviewSchema

posts_api = Blueprint('posts_api', __name__)


def _manage_post_by_type(post_type, data, post, is_edit=False):
    if post_type.post_type_name == 'Comment':
        details = data.get('comment')
        if not details:
            return jsonify(error='Comment body missing or malformed'), 400

        rev = Review(post)
        comment = Comment(review=rev, **details, edit=is_edit)
        db.session.add(comment)
        db.session.commit()
        
        return ReviewSchema().dumps(rev)

    if post_type.post_type_name == 'Rating':
        details = data.get('rating')
        if not details:
            return jsonify(error='Rating value missing or malformed'), 400

        rev = Review(post)
        rating = Rating(review=rev, **details, edit=is_edit)
        db.session.add(rating)
        db.session.commit()
        
        return ReviewSchema().dumps(rev)

    if post_type.post_type_name == 'Review':
        details = data.get('review')
        if not details:
            return jsonify(error='Review missing or malformed'), 400

        rev = Review(post)
        comment = Comment(review=rev, body=details.get('body'), edit=is_edit)
        rating = Rating(
            review=rev, rating_val=details.get('rating_val'), edit=is_edit)
        db.session.add(rating)
        db.session.add(comment)
        db.session.commit()
        
        return ReviewSchema().dumps(rev)

    if post_type.post_type_name == 'Amenity Tag':
        details = data.get('amenity_tag')
        if not details:
            return jsonify(error='Amenity id missing or malformed'), 400

        amenity_type = AmenityType.query.get(details.get('amenity_id'))
        amenity_tag = AmenityTag(amenity_type, post, edit=is_edit)

        db.session.add(amenity_tag)
        db.session.commit()
        
        return AmenityTagSchema().dumps(amenity_tag)

    if post_type.post_type_name == 'Promotion':
        details = data.get('promotion')
        if not details:
            return jsonify(error='Promotion missing or malformed'), 400

        promo = Promotion(post=post, **details, edit=is_edit)
        db.session.add(promo)
        db.session.commit()
        
        return PromotionSchema().dumps(promo)

    if post_type.post_type_name == 'Gas Price Suggestion':
        details = data.get('gas_price_suggestion')
        if not details:
            return jsonify(error='Gas price suggestion missing or malformed'), 400

        gas_post = GasPriceSuggestion(post, edit=is_edit)

        gases = []
        for gas in details.get('gases'):
            gas_type = GasType.query.get(gas.get('gas_type_id'))
            gases.append(Gas(details.get('price'), gas_type, gas_post))

        db.session.add(gas_post)
        db.session.add_all(gases)
        db.session.commit()
        
        return GasPriceSuggestionSchema().dumps(gas_post)


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
        - 404 if the post requested to be edited is not found or deleted
        - 405 if the user is trying to edit a post after the 30 minute window
        - 500 if the request failed on the server side
    """
    if request.method == 'POST':
        try:
            data = HandlePostSchema(context={'method': request.method}, exclude=('post_id',)).load(request.get_json(
                force=True, silent=True) or request.form.to_dict())

            post_type: PostType = PostType.query.get(data.get('post_type_id'))

            if not (post_type in g.current_user.user_type.allowed_post_types):
                return jsonify(error=f'This user is not allowed to make {post_type.post_type_name} posts'), 403

            gas_station: GasStation = GasStation.query.get(
                data.get('gas_station_id'))

            post = Post(gas_station, post_type, g.current_user)

            resdata = _manage_post_by_type(post_type, data, post)

            return jsonify(message='Post created successfully', data=resdata), 200

        except ValidationError as e:
            return jsonify(errors=e.messages), 400

    if request.method == 'PUT':
        try:
            data = HandlePostSchema(context={'method': request.method}, exclude=('gas_station_id', 'post_type_id')).load(request.get_json(
                force=True, silent=True) or request.form.to_dict())

            post: Post = Post.query.get(data.get('post_id'))

            if not post:
                return jsonify(error='The specified post does not exist'), 404

            if post.deleted_at:
                return jsonify(error='The specified post has been deleted'), 404

            if (post.created_at + timedelta(minutes=30)) < datetime.utcnow():
                return jsonify(error='The 30-minute modification window has passed for the specified post'), 405

            resdata = _manage_post_by_type(post.post_type, data, post, True)

            return jsonify(message='The post has been updated successfully', data=resdata)

        except ValidationError as e:
            return jsonify(errors=e.messages), 400

    if request.method == 'DELETE':
        try:
            data = HandlePostSchema(context={'method': request.method}, only=('post_id',)).load(request.get_json(
            force=True, silent=True) or request.form.to_dict())
        
            post: Post = Post.query.get(data.get('post_id'))

            if not post:
                return jsonify(error='The specified post does not exist'), 404

            if post.deleted_at:
                return jsonify(error='The specified post has been deleted already'), 404

            if (post.created_at + timedelta(minutes=30)) < datetime.utcnow():
                return jsonify(error='The 30-minute modification window has passed for the specified post'), 405
            
            post.deleted_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify(message='The post was successfully deleted'),200
        except ValidationError as e:
            return jsonify(errors=e.messages), 400
    else:
        return jsonify(error='method not allowed'),405

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
        data = PostVoteSchema().load(request.get_json(
            force=True, silent=True) or request.form.to_dict())

        post: Post = Post.query.get(data.get('post_id'))

        if post:
            if post.deleted_at:
                return jsonify(error='The specified post has been deleted'), 404

            if not post.post_type.is_votable:
                return jsonify(error='The type of the specified post is not votable'), 405

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
        - 403 If the user's type is not allowed to upvote
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
    return _vote_on_post('Upvote toggled successfully', 'downvoters', 'upvoters')


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
        - is_votable (bool)

    Body for PUT:    
        - post_type_name (str)
        - is_votable (bool)
        - id (int)

    Returns with message:
        - 200 if the request was successful
        - 400 if the request body was malformed for the method
        - 403 If the user making the request is not an admin
        - 404 if the post type to be edited could not be found
        - 500 if the server fails to carry out the request
    """
    if request.method == 'POST':
        try:
            # try to create a new post type

            # validate request body
            data = HandlePostTypesSchema(exclude=('id',)).load(request.get_json(
                force=True, silent=True) or request.form.to_dict())

            ptype = PostType(**data)
            db.session.add(ptype)
            db.session.commit()
        except ValidationError as e:
            return jsonify(errors=e.messages), 400
        except IntegrityError:
            return jsonify(error='This post type already exists'), 409

        return jsonify(message='Post type added successfully'), 200

    elif request.method == 'PUT':
        try:
            # try to update the post type

            # validate request body
            data = HandlePostTypesSchema().load(request.get_json(
                force=True, silent=True) or request.form.to_dict())

            ptype = PostType(**data)
            db.session.merge(ptype)
            db.session.commit()
        except ValidationError as e:
            return jsonify(errors=e.messages), 400

        return jsonify(message='User type modified successfully'), 200

    elif request.method == 'GET':
        # get all the post types in the DB
        data = PostTypeSchema(many=True).dump(PostType.query.all())
        return jsonify(message='Fetch successful', data=data), 200

    else:
        return jsonify(error='method not allowed'), 405


app.register_blueprint(posts_api, url_prefix='/posts')
