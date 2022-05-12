import json
from datetime import datetime

from config import app, db
from controller.routes.token import gen_access_refresh_token, token_required
from controller.utils import get_request_body
from controller.validation.schemas import EditUserSchema
from flask import Blueprint, g, jsonify, request
from marshmallow import ValidationError
from model.schemas import UserSchema
from sqlalchemy.exc import IntegrityError

user_api = Blueprint('user_api', __name__)


@user_api.route('', methods=['DELETE', 'PUT'])
@token_required
def edit_user():
    """
    Endpoint for editing or deleting a user

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
        g.current_user.deleted_at = datetime.utcnow()
        db.session.merge(g.current_user)
        db.session.commit()
    if request.method == 'PUT':
        try:
            data: dict = EditUserSchema().load(get_request_body())
            userdata = UserSchema().dump(g.current_user)

            # merge old user data and updated fields
            updated = {**userdata, 'password': None, **data}

            user = UserSchema().load(updated)

            if user.password == None:
                user._password = g.current_user.password

            db.session.merge(user)
            db.session.commit()

            # give the user a new token
            res = gen_access_refresh_token(user)
            body = res.json()
            body['message'] = 'User updated successfully'
            res.data = json.dumps(body)
            return res, 200

        except IntegrityError as e:
            return jsonify(error='Email address is already in use'), 409

        except ValidationError as e:
            return jsonify(errors=e.messages), 400

    else:
        return jsonify(error='Method not allowed'), 405


app.register_blueprint(user_api, url_prefix='/users')
