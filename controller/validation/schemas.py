from marshmallow import Schema, validate, validates, ValidationError, fields


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

    email = fields.Email(required=True)

    firstname = fields.Str(required=True, validate=[validate.Regexp(
        '^[A-Z][a-z]*(([-]| )[A-Z][a-z]*)?$', 0, error='Invalid characters in the first name')])

    lastname = fields.Str(required=True, validate=[validate.Regexp(
        '^[A-Z][a-z]*(([-]| )[A-Z][a-z]*)?$', 0, error='Invalid characters in the last name')])


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
            email_val = validate.Email()
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
                iden = len_val.__call__(val)
            except ValidationError as e2:
                errors.append(str(e2))
            try:
                iden = reg_val.__call__(val)
            except ValidationError as e3:
                errors.append(str(e3))

            # if there are validation errors then fail the validation
            if errors:
                errors.append(str(e))
                raise ValidationError(errors+['Not a valid username or email'])

        # pass the validation if its a valid email or username
        return str(iden)
