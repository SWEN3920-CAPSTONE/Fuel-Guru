from datetime import datetime
import json

from config import app, db
from controller.routes.token import (admin_required, gen_access_refresh_token,
                                     token_required)
from controller.utils import get_request_body
from controller.validation.schemas import EditUserSchema, HandleUserTypesSchema
from flask import Blueprint, g, jsonify, request
from marshmallow import ValidationError
from model import UserType
from model.schemas import UserSchema, UserTypeSchema
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


@user_api.route('/types', methods=['POST', 'PUT', 'GET'])
@admin_required
def user_types():
    """
    Endpoint for handling user types

    Body for POST:
        - user_type_name
        - is_admin

    Body for PUT:
        - user_type name
        - is_admin
        - id

    Returns with message:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not an admin
        - 409 if the user type already exists in a POST request
        - 500 if there was a server error
    """

    if request.method == 'POST':
        try:
            # try to create a new user type

            # validate request body
            data = HandleUserTypesSchema(
                exclude=('id',)).load(get_request_body())

            utype = UserType(**data)
            db.session.add(utype)
            db.session.commit()
        except ValidationError as e:
            return jsonify(errors=e.messages), 400
        except IntegrityError:
            return jsonify(error='This user type already exists'), 409

        return jsonify(message='User type added successfully'), 200

    elif request.method == 'PUT':
        try:
            # try to update the user type

            # validate request body
            data = HandleUserTypesSchema().load(get_request_body())

            utype = UserType(**data)
            db.session.merge(utype)
            db.session.commit()
        except ValidationError as e:
            return jsonify(errors=e.messages), 400

        return jsonify(message='User type modified successfully'), 200

    elif request.method == 'GET':
        # get all the user types in the DB
        data = UserTypeSchema(many=True).dump(UserType.query.all())
        return jsonify(message='Fetch successful', data=data), 200

    else:
        return jsonify(error='method not allowed'), 405


app.register_blueprint(user_api, url_prefix='/users')
