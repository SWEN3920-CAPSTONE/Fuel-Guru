from config import app, db
from controller.routes.token import admin_required
from controller.utils import get_request_body
from controller.validation.schemas import HandleUserTypesSchema
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from model.users import UserType
from sqlalchemy.exc import IntegrityError

admin_api = Blueprint('admin_api',__name__)

def _admin_type_ops(RouteSchema, Model, type_name:str, *, post_schema_kwargs=dict(), put_schema_kwargs=dict()):
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
        data = RouteSchema(many=True).dump(Model.query.all())
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
    _admin_type_ops()

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
    pass
    _admin_type_ops()
    

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

    return _admin_type_ops(HandleUserTypesSchema,UserType, 'user', post_schema_kwargs={'exclude':('id',)})


@admin_api.route('gasstations',methods=['POST', 'PUT','DELETE'])
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
        - (and at least one of the following)
            - name
            - address
            - lat
            - lng
            - image
            - manager_id
        
    Body for DELETE:
        - id
        
    Returns with message:
        - 200 If the request was sucessful
        - 400 if the request is malformed
        - 401 if the user making the request is not logged in
        - 403 if the user making the request is not an admin
        - 500 if there was a server error
    """
    pass


@admin_api.route('/gasstations/manager', methods=['POST'])
@admin_required
def add_gasstation_manager():
    """
    Endpoint for specialised signup for gas station managers

    Body:
        - username (str)
        - password (str)
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
    pass

app.register_blueprint(admin_api, url_prefix='/admin')
