import json
from datetime import datetime

from config import app, db
from controller.routes.token import gen_jwts, token_required
from controller.utils import get_request_body
from controller.validation.schemas import EditUserSchema
from flask import Blueprint, g, jsonify, request
from marshmallow import ValidationError
from model.schemas import UserSchema
from sqlalchemy.exc import IntegrityError

user_api = Blueprint('user_api', __name__)


@user_api.route('', methods=['DELETE', 'PUT', 'GET'])
@token_required
def normal_users():
    """
    Endpoint for editing or deleting a user or getting the user profile

    No body for DELETE

    Body for PUT (at least one of the following):
        - [firstname]
        - [lastname]
        - [both:
            - current_email
            - new_email] 
        - [both:
            - current_password
            - new_password]

    Returns with message:
        - 200 if the request was successful
        - 400 if the body was empty for PUT or otherwise malformed
        - 401 if the user making the request isnt logged in
        - 403 if the current_password or current_email are incorrect
        - 409 if the new_email is already in use
        - 500 for server error
    """
    if request.method == 'DELETE':
        # set deleted_at to now
        g.current_user.deleted_at = datetime.utcnow()
        db.session.merge(g.current_user)
        db.session.commit()        
        return jsonify(message='Successfully deleted this user'), 200
    if request.method == 'PUT':
        try:
            data: dict = EditUserSchema().load(get_request_body())
            
            if data.get('current_password'):
                if not g.current_user.check_password(data.get('current_password')):
                    return jsonify(message='Current password is incorrect'), 403
                else:
                    data.pop('current_password')
            
            if data.get('current_email'):
                if not g.current_user.email == data.get('current_email'):
                    return jsonify(message='Current email is incorrect'), 403
                else:
                    data.pop('current_email')
            
            
            userdata:dict = UserSchema().dump(g.current_user)
            userdata.get('user_type').pop('allowed_post_types')
            userdata.pop('managed_gasstations', None)

            # merge old user data and updated fields
            updated = {**userdata, **data}
            
            user = UserSchema().load(updated)

            if not data.get('password'):
                # In the case where a password isnt being changed, 
                # we dont need to rehash it
                user._password = g.current_user.password

            db.session.merge(user)
            db.session.commit()
            print(user)
            # give the user a new token set
            res = gen_jwts(user)
            body = res.json()
            body.update({'message': 'User profile updated successfully', 'data': UserSchema().dump(user)})
            res.data = json.dumps(body)
            return res, 200

        except IntegrityError as e:
            return jsonify(error='Email address is already in use'), 409

        except ValidationError as e:
            return jsonify(errors=e.messages), 400

    if request.method == 'GET':
        return jsonify(message='Data fetched successfully', data=UserSchema().dump(g.current_user))
    else:
        return jsonify(error='Method not allowed'), 405


app.register_blueprint(user_api, url_prefix='/users')
