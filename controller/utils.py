from datetime import datetime, timedelta
from uuid import uuid4
from flask import flash, request, url_for
import jwt
from config import app


def get_request_body():
    return request.get_json(force=True, silent=True) or request.form.to_dict()


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')
            
def generate_reset_link(user, html=True):
    """
    Generate a password reset link

    Args:
        user (User):
            The user to generate the link for

        html (bool):
            True to return a section of html in as a string or the link by itself as a string

    Returns:
        str -> the change link or html with the change link
    """

    change_token = jwt.encode({
        'type': 'reset',
        'sub': user.id,
        'jti': uuid4().hex,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, key=app.config.get('SECRET_KEY'))

    link = f"{request.root_url}/{url_for('auth_api.reset_user_password', token=change_token)}"

    section = f"""
    <br><br>You may change your password by using the link below:
    <br><a href="{link}"> {link}</a>
        
    <br><br> This link will be valid for 30 minutes
    
    <br><br>If this was not done by you, you may ignore this email.
    """

    return section if html else link