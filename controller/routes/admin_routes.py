from uuid import uuid4

from config import app, db, mail
from controller.routes.token import admin_required
from controller.utils import generate_reset_link, get_request_body
from controller.validation.schemas import (HandleAmenityTypesSchema,
                                           HandleGasStationsSchema,
                                           HandleGasTypesSchema,
                                           HandlePostTypesSchema,
                                           HandleUserTypesSchema, SignupSchema)
from flask import Blueprint, jsonify, request
from flask_mail import Message
from marshmallow import ValidationError
from model.gasstation import GasStation
from model.posts import AmenityType, GasType, PostType
from model.schemas import (AmenityTypeSchema, GasStationSchema, GasTypeSchema,
                           PostTypeSchema, UserTypeSchema)
from model.users import User, UserType
from sqlalchemy.exc import IntegrityError

admin_api = Blueprint('admin_api', __name__)


def _admin_type_ops(RouteSchema, Model, ModelSchema, type_name: str, *, post_schema_kwargs=dict(), put_schema_kwargs=dict()):
    if request.method == 'POST':
        try:
            # try to create a new user type

            # validate request body
            data = RouteSchema(
                **post_schema_kwargs).load(get_request_body())
            model = Model(**data)
            db.session.add(model)
            db.session.commit()
        except ValidationError as e:
            return jsonify(errors=e.messages), 400
        except IntegrityError:
            return jsonify(error=f'This {type_name.lower()} type already exists'), 409

        return jsonify(message=f'{type_name.capitalize()} type added successfully'), 200

    elif request.method == 'PUT':
        try:
            # try to update the user type

            # validate request body
            data = RouteSchema(**put_schema_kwargs).load(get_request_body())

            model = Model(**data)
            db.session.merge(model)
            db.session.commit()
        except ValidationError as e:
            return jsonify(errors=e.messages), 400

        return jsonify(message=f'{type_name.capitalize()} type modified successfully'), 200

    elif request.method == 'GET':
        # get all the user types in the DB
        data = ModelSchema(many=True).dump(Model.query.all())
        return jsonify(message='Fetch successful', data=data), 200

    else:
        return jsonify(error='method not allowed'), 405


@admin_api.route('/amenities/types', methods=['POST', 'PUT', 'GET'])
@admin_required
def amenity_types():
    """
    Endpoint for handling amenity types

    Body for POST:
        - amenity_name

    Body for PUT:
        - id 
        - amenity_name

    Returns with message:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not an admin
        - 500 if there was a server error
    """
    return _admin_type_ops(HandleAmenityTypesSchema, AmenityType, AmenityTypeSchema, 'amenity', post_schema_kwargs={'exclude': ('id',)})


@admin_api.route('/gas/types', methods=['POST', 'PUT', 'GET'])
@admin_required
def gas_types():
    """
    Endpoint for handling gas types

    Body for POST:
        - gas_type_name

    Body for PUT:
        - id 
        - gas_type_name

    Returns with message:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not an admin
        - 500 if there was a server error
    """
    return _admin_type_ops(HandleGasTypesSchema, GasType, GasTypeSchema, 'gas', post_schema_kwargs={'exclude': ('id',)})


@admin_api.route('/users/types', methods=['POST', 'PUT', 'GET'])
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

    return _admin_type_ops(HandleUserTypesSchema, UserType, UserTypeSchema, 'user', post_schema_kwargs={'exclude': ('id',)})


@admin_api.route('/gasstations', methods=['POST', 'PUT'])
@admin_required
def gasstations():
    """
    Endpoint for handling gas stations

    Body for POST:
        - name
        - address
        - lat
        - lng
        - [image]
        - [manager_id]

    Body for PUT:
        - id 
        - name
        - address
        - lat
        - lng
        - image
        - manager_id

    Returns with message:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not an admin
        - 404 if a manager was provided and cannot be found
        or if the gas station cannot be found
        - 500 if there was a server error
    """
    try:
        if request.method == 'POST':
            data: dict = HandleGasStationsSchema(
                exclude=('id',)).dump(get_request_body())

            if data.get('manager_id'):
                manager = User.query.get(data.get('manager_id'))
                if not manager:
                    return jsonify(error='The user specified to be the manager was not found'), 404
            else:
                manager = None

            station = GasStation(**data, manager=manager)

            db.session.add(station)
            db.session.commit(station)

            return jsonify(message='Gas station added successfully'), 400

        if request.method == 'PUT':
            data: dict = HandleGasStationsSchema(partial=(
                'name', 'address', 'lat', 'lng', 'image', 'manager_id')).dump(get_request_body())

            station = GasStation.query.get(data.get('id'))

            if not station:
                return jsonify(error='The specified station does not exist'), 404

            if data.get('manager_id'):
                manager = User.query.get(data.get('manager_id'))
                data.pop('manager_id')
                if not manager:
                    return jsonify(error='The user specified to be the manager was not found'), 404
            else:
                manager = station.manager

            existing = GasStationSchema().dump(station)

            updated = GasStation(**existing, manager=manager, **data)

            db.session.merge(updated)
            db.session.commit()

            return jsonify(message='The gas station has been successfully updated'), 200
    except ValidationError as e:
        return jsonify(errors=e.messages), 400


@admin_api.route('/gasstations/manager', methods=['POST'])
@admin_required
def add_gasstation_manager():
    """
    Endpoint for specialised signup for gas station managers

    Body:
        - username (str)
        - email (str)
        - firstname (str)
        - lastname (str)

    Returns with message:
        - 200 if successful and a JWT to be stored in the client-side
        - 400 if the body sent with the request was malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not authorized to
        - 500 If the server failed to carry out the request 
    """
    try:
        data = SignupSchema(exclude=('password','username')).dump(get_request_body())
        passwd = uuid4().hex
        uname = uuid4().hex

        user_type = UserType.query.filter_by(
            user_type_name='Gas Station Manager').first()

        manager = User(**data, password=passwd,username=uname, user_type=user_type)
        
        db.session.add(manager)
        db.session.commit()

        change_link = generate_reset_link(manager, is_manager=True)

        # very basic, no styling lol
        ehtml = f"""
        Welcome to Fuel Guru {manager.firstname} {manager.lastname}. 
        <br> You have been added as a gas station manager.
        <br>
        
        <br>username: {manager.username}
        <br>email: {manager.email}
        
        {change_link}        
        """

        msg = Message('Welcome to FuelGuru', recipients=[
                      manager.email], html=ehtml)

        # using gmail to send
        mail.send(msg)

        return jsonify(message='Add gas station manager success'), 200

    except ValidationError as e:
        return jsonify(errors=e.messages), 400


@admin_api.route('/posts/types', methods=['POST', 'PUT', 'GET'])
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
    return _admin_type_ops(HandlePostTypesSchema, PostType, PostTypeSchema, 'post', post_schema_kwargs={'exclude': ('id',)})


app.register_blueprint(admin_api, url_prefix='/admin')
