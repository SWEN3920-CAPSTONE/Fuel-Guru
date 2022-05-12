from marshmallow import Schema, post_load, validate, validates, ValidationError, fields, validates_schema


class SignupSchema(Schema):
    """
    Schema to validate the data sent to the signup route for normal users
    """

    username = fields.Str(required=True, validate=[
        validate.Length(
            5, 30, error='The username must be at least 5 characters long and at most 30 characters long'),
        validate.Regexp(
            '^[A-Za-z]+([0-9A-Za-z]+\_?)*[0-9A-Za-z]+$',
            0,
            error='The username must contain uppercase letters, lowercase letters, numbers and underscores only')])

    password = fields.Str(required=True, validate=[
        validate.Regexp('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!-&@~])[A-Za-z0-9!-&@~]+$', 0,
                          error='The password must have at least 1 uppercase, 1 lowercase letter, 1 number and 1 special character'),
        validate.Length(min=12, error='The password must be at least 12 characters')])

    email = fields.Email(required=True, validate=[
                         validate.Length(min=1, max=255)])

    firstname = fields.Str(required=True, validate=[validate.Regexp(
        '^[A-Z][a-z]*(([-]| )[A-Z][a-z]*)?$', 0, error='Invalid characters in the first name'), validate.Length(min=1, max=255)])

    lastname = fields.Str(required=True, validate=[validate.Regexp(
        '^[A-Z][a-z]*(([-]| )[A-Z][a-z]*)?$', 0, error='Invalid characters in the last name'), validate.Length(min=1, max=255)])


class SigninSchema(Schema):
    """
    Schema to validate data sent to the signin route
    """

    iden = fields.Str(required=True)
    """Username or Email"""

    password = fields.Str(required=True, validate=[
        validate.Regexp('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!-&@~])[A-Za-z0-9!-&@~]+$', 0,
                          error='The password must have at least 1 uppercase, 1 lowercase letter, 1 number and 1 special character'),
        validate.Length(min=12, error='The password must be at least 12 characters')])

    @validates('iden')
    def validate_iden(self, val):
        """
        Checks that iden is either a valid username or valid email
        """

        errors = []
        iden = None
        try:
            # try to validate iden as email address
            email_val = validate.And(
                validate.Email(), validate.Length(min=1, max=255))
            iden = email_val.__call__(val)
        except ValidationError as e:
            # on failure, try to validate iden as a username
            len_val = validate.Length(
                5, 30, error='The username must be at least 5 characters long and at most 30 characters long')
            reg_val = validate.Regexp(
                '^[A-Za-z]+([0-9A-Za-z]+\_?)*[0-9A-Za-z]+$',
                0,
                error='The username must contain uppercase letters, lowercase letters, numbers and underscores only')

            # add the validation errors that have been raised to errors
            try:
                iden = validate.And(len_val, reg_val).__call__(val)
            except ValidationError as e2:
                errors.append(str(e2))

            # if there are validation errors then fail the validation
            if errors:
                errors.append(str(e))
                raise ValidationError(errors+['Not a valid username or email'])

        # pass the validation if its a valid email or username
        return str(iden)


class HandleUserTypesSchema(Schema):

    id = fields.Int(required=True, strict=True)

    user_type_name = fields.Str(required=True, validate=[
                                validate.Regexp('[A-Za-z]+( [A-Za-z]+)*'),
                                validate.Length(min=1, max=255)])

    is_admin = fields.Boolean(required=True,
                              truthy={'true', 'TRUE', 'True'},
                              falsy={'FALSE', 'false', 'False'})


class EditUserSchema(Schema):
    firstname = fields.Str(validate=[validate.Length(min=1, max=255),
                                     validate.Regexp(
        '^[A-Z][a-z]*(([-]| )[A-Z][a-z]*)?$', 0, error='Invalid characters in the first name')])

    lastname = fields.Str(validate=[validate.Length(min=1, max=255),
                                    validate.Regexp(
        '^[A-Z][a-z]*(([-]| )[A-Z][a-z]*)?$', 0, error='Invalid characters in the last name')])

    current_email = fields.Email(validate=[validate.Length(min=1, max=255)])

    new_email = fields.Email(validate=[validate.Length(min=1, max=255)])

    current_password = fields.Str(validate=[
        validate.Regexp('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!-&@~])[A-Za-z0-9!-&@~]+$', 0,
                        error='The current password must have at least 1 uppercase, 1 lowercase letter, 1 number and 1 special character'),
        validate.Length(min=12, error='The current password must be at least 12 characters')])

    new_password = fields.Str(validate=[
        validate.Regexp('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!-&@~])[A-Za-z0-9!-&@~]+$', 0,
                        error='The new password must have at least 1 uppercase, 1 lowercase letter, 1 number and 1 special character'),
        validate.Length(min=12, error='The new password must be at least 12 characters')])

    @validates_schema
    def validate_form(self, data: dict, **kwargs):

        email_provided = data.get('current_email') and data.get('new_email')
        password_provided = data.get(
            'current_password') and data.get('new_password')

        if not (email_provided or password_provided or data.get('firstname') or data.get('lastname')):
            raise ValidationError('No data provided')

        errors = []
        if bool(data.get('current_email')) ^ bool(data.get('new_email')):
            errors.append('Both current email and new email must be provided')

        if bool(data.get('current_password')) ^ bool(data.get('new_password')):
            errors.append(
                'Both current password and new password must be provided')

        if errors:
            raise ValidationError(errors)

        return True


    @post_load
    def remove_invalid_keys(self, data: dict, **kwargs):
        data.pop('current_password', None)
        data.pop('current_email', None)

        email = data.pop('new_email', None)
        password = data.pop('new_password', None)

        if email:
            data['email'] = email
            
        if password:
            data['password'] = password

        return data
