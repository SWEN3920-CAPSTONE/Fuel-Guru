from re import M
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired, Regexp, Length

_password_reg = Regexp('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!-&@~])[A-Za-z0-9!-&@~]+$', 0,
                       'The password must have at least 1 uppercase, 1 lowercase letter, 1 number and 1 special character')

_username_reg = Regexp(
    '^[A-Za-z]+([0-9A-Za-z]+\_?)*[0-9A-Za-z]+$',
    0, 'The username must contain uppercase letters, lowercase letters, numbers and underscores only. It must start with a letter and cannot end with an underscore')


class ResetPassword(FlaskForm):
    password = PasswordField(
        validators=[InputRequired(), _password_reg, Length(min=12)])

    conf_password = PasswordField('Confirm Password', validators=[
                                  InputRequired(), _password_reg])
    
class ResetPasswordManager(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(
        min=5, max=30, message='The username must be at least 5 characters long and at most 30 characters long'), _username_reg])

    password = PasswordField(
        validators=[InputRequired(), _password_reg, Length(min=12)])

    conf_password = PasswordField('Confirm Password', validators=[
                                  InputRequired(), _password_reg])
