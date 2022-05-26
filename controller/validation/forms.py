from re import M
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import InputRequired, Regexp, Length

_password_reg = Regexp('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!-&@~])[A-Za-z0-9!-&@~]+$', 0,
                       'The password must have at least 1 uppercase, 1 lowercase letter, 1 number and 1 special character')


class ResetPassword(FlaskForm):
    password = PasswordField(
        validators=[InputRequired(), _password_reg, Length(min=12)])
    
    conf_password = PasswordField('Confirm Password', validators=[
                                  InputRequired(), _password_reg])
