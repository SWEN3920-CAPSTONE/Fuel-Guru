from config import app, db
from controller.routes.token import admin_required, token_required
from flask import Blueprint, abort, g, jsonify, make_response, request
from flask_wtf.csrf import generate_csrf
from model.gasstation import GasStation
from model.posts import (AmenityTag, AmenityType, Comment, Gas,
                         GasPriceSuggestion, GasType, Post, PostType,
                         Promotion, Rating, Review)
from model.users import User, UserType
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError


@app.after_request
def setheaders(resp):
    if resp == None:
        resp = make_response()
    # to protect form submissions
    # more research needed
    resp.set_cookie('CSRF-TOKEN', generate_csrf(), samesite='Lax')
    return resp


@app.route('/amenities/types', methods=['POST', 'PUT', 'GET'])
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
    pass


@app.route('/gas/types', methods=['POST', 'PUT', 'GET'])
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


@app.errorhandler(HTTPException)
def http_error(err: HTTPException):
    return jsonify(error=err.description), err.code


@app.errorhandler(SQLAlchemyError)
def sqlalchemy_error(err: SQLAlchemyError):
    return jsonify(error=f'Database error: {str(err)} with code {err.code}'), 500
