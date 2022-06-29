from config import app, db
from flask import jsonify, make_response
from flask_wtf.csrf import generate_csrf
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError


@app.after_request
def setheaders(resp):
    if resp == None:
        resp = make_response()
    # to protect form submissions
    # more research needed
    resp.set_cookie('CSRF-TOKEN', generate_csrf(), samesite='Lax')
    print(resp.data)
    return resp


@app.errorhandler(HTTPException)
def http_error(err: HTTPException):
    return jsonify(error=err.description), err.code


@app.errorhandler(SQLAlchemyError)
def sqlalchemy_error(err: SQLAlchemyError):
    db.session.rollback()
    return jsonify(error=f'Database error: {str(err)} with code {err.code}'), 500
