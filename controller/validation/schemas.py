from flask import escape
from marshmallow import Schema, post_load, validate, validates, ValidationError, fields, validates_schema


class EscStr(fields.Str):

    def _deserialize(self, value, attr, data, **kwargs):
        return super()._deserialize(str(escape(value)), attr, data, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        return super()._serialize(str(escape(value)), attr, obj, **kwargs)


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
            error='The username must contain uppercase letters, lowercase letters, numbers and underscores only. It must start with a letter and cannot end with an underscore')])

    password = fields.Str(required=True, validate=[
        validate.Regexp('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!-+@^_~])[A-Za-z0-9!-+@^_~]+$', 0,
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
        validate.Regexp('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!-+@^_~])[A-Za-z0-9!-+@^_~]+$', 0,
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

    can_vote = fields.Boolean(required=True,
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
        validate.Regexp('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!-+@^_~])[A-Za-z0-9!-+@^_~]+$', 0,
                        error='The current password must have at least 1 uppercase, 1 lowercase letter, 1 number and 1 special character'),
        validate.Length(min=12, error='The current password must be at least 12 characters')])

    new_password = fields.Str(validate=[
        validate.Regexp('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!-+@^_~])[A-Za-z0-9!-+@^_~]+$', 0,
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


class PostVoteSchema(Schema):

    post_id = fields.Integer(required=True, strict=True)


class HandlePostTypesSchema(Schema):
    id = fields.Int(required=True, strict=True)

    post_type_name = fields.Str(required=True, validate=[
                                validate.Regexp('[A-Za-z]+( [A-Za-z]+)*'),
                                validate.Length(min=1, max=255)])

    is_votable = fields.Boolean(required=True,
                                truthy={'true', 'TRUE', 'True'},
                                falsy={'FALSE', 'false', 'False'})


class HandlePostSchema(Schema):
    # internal schemas
    class PostComment(Schema):
        body = EscStr(required=True, validate=[
            validate.Length(min=1, max=500)])

    class PostRating(Schema):
        rating_val = fields.Integer(required=True, strict=True, validate=[
                                    validate.Range(min=1, max=5)])

    class PostPromotion(Schema):
        desc = EscStr(required=True, validate=[
            validate.Length(min=1, max=255)])

        start_date = fields.DateTime(required=True)

        end_date = fields.DateTime(required=True)

        image = EscStr(required=False, allow_none=True)

    class PostReview(Schema):
        rating_val = fields.Integer(required=True, strict=True, validate=[
                                    validate.Range(min=1, max=5)])

        body = EscStr(required=True, validate=[
            validate.Length(min=1, max=500)])

    class PostAmenity(Schema):
        amenity_id = fields.Int(required=True, strict=True)

    class PostGasPriceSuggestion(Schema):
        class PostGas(Schema):
            gas_type_id = fields.Int(required=True, strict=True)

            price = fields.Decimal(required=True, allow_nan=False, validate=[
                validate.Range(min=1)])

        gases = fields.Nested(PostGas, many=True, required=True)

        @validates('gases')
        def at_least_one_gas(self, val, **kwargs):
            if len(val) >= 1:
                return val
            else:
                raise ValidationError('At least one gas must be provided')

    ###################

    post_id = fields.Int(required=True, strict=True)  # PUT, DELETE

    gas_station_id = fields.Int(required=True, strict=True)  # POST

    post_type_id = fields.Int(required=True, strict=True)  # POST

    comment = fields.Nested(PostComment)

    rating = fields.Nested(PostRating)

    promotion = fields.Nested(PostPromotion)

    review = fields.Nested(PostReview)

    amenity_tag = fields.Nested(PostAmenity)

    gas_price_suggestion = fields.Nested(PostGasPriceSuggestion)

    @validates_schema
    def validate_post_data(self, data: dict, **kwargs):
        # check if some data has been provided
        some_posts = data.get('promotion')\
            or data.get('rating')\
            or data.get('review')\
            or data.get('amenity_tag')\
            or data.get('gas_price_suggestion')\
            or data.get('comment')

        data_provided = data.get('post_id') \
            or data.get('gas_station_id')\
            or data.get('post_type_id') \
            or some_posts

        if data_provided:
            if some_posts and (self.context.get('method') == 'POST' or self.context.get('method') == 'PUT'):
                # xor the posts
                single_post = bool(data.get('promotion'))\
                    ^ bool(data.get('comment')) \
                    ^ bool(data.get('gas_price_suggestion'))\
                    ^ bool(data.get('review'))\
                    ^ bool(data.get('rating'))\
                    ^ bool(data.get('amenity_tag'))

                if not single_post:
                    raise ValidationError(
                        'Only one type of post\'s data should be provided')

                return True

            if not some_posts and (self.context.get('method') == 'POST' or self.context.get('method') == 'PUT'):
                raise ValidationError(
                    'Post details should be sent in a POST or PUT method')

            if some_posts and self.context.get('method') == 'DELETE':
                raise ValidationError(
                    'No post details should be included in a delete request')

            return True
        else:
            raise ValidationError('No data provided')


class HandleGasTypesSchema(Schema):
    id = fields.Int(required=True, strict=True)

    gas_type_name = EscStr(required=True, validate=[
        validate.Length(min=1, max=255)])


class HandleAmenityTypesSchema(Schema):
    id = fields.Int(required=True, strict=True)

    amenity_name = EscStr(required=True, validate=[
        validate.Length(min=1, max=255)])


class HandleGasStationsSchema(Schema):
    id = fields.Int(required=True, strict=True)

    name = EscStr(required=True, validate=[validate.Length(min=1, max=255)])

    address = EscStr(required=True, validate=[
        validate.Length(min=1, max=255)])

    lat = fields.Decimal(required=True)

    lng = fields.Decimal(required=True)

    image = EscStr()

    manager_id = fields.Int(strict=True)

    @validates_schema
    def at_least_one_field(self, data, **kwargs):
        if self.partial:
            data_provided = data.get('address') \
                or data.get('lat') \
                or data.get('lng') \
                or data.get('image') \
                or data.get('manager_id') \
                or data.get('name')

            if bool(data_provided) and bool(data.get('id')):
                return True
            else:
                raise ValidationError(
                    'Data for at least one field other than id must be provided')
        return True


class GasStationSearchSchema(Schema):
    name = EscStr(validate=[
        validate.Length(min=1, max=255)])

    cheapest = fields.Bool(truthy={'true', 'TRUE', 'True'},
                           falsy={'FALSE', 'false', 'False'}, load_default=False)

    nearest = fields.Bool(truthy={'true', 'TRUE', 'True'},
                          falsy={'FALSE', 'false', 'False'}, load_default=False)
    
    lat = fields.Float()
    
    lng = fields.Float()    

    @validates_schema
    def at_least_one_field(self, data, **kwargs):            
        if data.get('nearest'):
            if not (bool(data.get('lat')) and bool(data.get('lng'))):
                raise ValidationError('Lat and lng must be provided if nearest is true', field_name='nearest')
        
        return True

class HandleUserLocationSchema(Schema):
    lat = fields.Decimal(required=True)

    lng = fields.Decimal(required=True)


class HandleUserGasstationLocationSchema(Schema):
    user_lat = fields.Decimal(required=True)

    user_lng = fields.Decimal(required=True)

    gs_lat = fields.Decimal(required=True)

    gs_lng = fields.Decimal(required=True)
