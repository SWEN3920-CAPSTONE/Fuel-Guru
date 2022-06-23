from datetime import datetime, timedelta
from time import timezone
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
            
def generate_reset_link(user,time_delta=30, html=True, is_manager=False, unit='minutes'):
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
        'exp': datetime.utcnow() + timedelta(**{unit:time_delta})
    }, key=app.config.get('SECRET_KEY'))

    link = f"{request.root_url}/{url_for('auth_api.reset_user_password' if is_manager==False else 'auth_api.reset_manager_info', token=change_token)}"

    section = f"""
    <br><br>You may make the change by using the link below:
    <br><a href="{link}"> {link}</a>
        
    <br><br> This link will be valid for {time_delta} {unit}
    
    <br><br>If this was not done by you, you may ignore this email.
    """

    return section if html else link

def utc_today():
    print(datetime.utcnow(), datetime.now(timezone.utc))
    return datetime.fromisoformat(datetime.utcnow().date().isoformat())