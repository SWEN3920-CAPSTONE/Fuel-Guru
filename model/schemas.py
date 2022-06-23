from datetime import datetime

from pytz import timezone
from config import ma
from marshmallow import fields, post_dump, post_load

from model.gasstation import GasStation
from model.posts import (AmenityTag, AmenityType, Gas,
                         GasPriceSuggestion, GasType, Post, PostType,
                         Promotion, Review)
from model.users import User, UserType


class JADateTime(fields.DateTime):
    """
    Custom DateTime field that converts from/to UTC to/from Jamaica time
    """
    
    def _deserialize(self, value, attr, data, **kwargs):
        return super()._deserialize(value, attr, data, **kwargs)
    
    def _serialize(self, value:datetime, attr, obj, **kwargs):
        value=value.astimezone(timezone('UTC'))
        return timezone('America/Jamaica').localize(value).isoformat()


class AmenityTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AmenityType
        include_relationships = True
        load_instance = True
        transient = True


class PromotionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Promotion
        include_relationships = True
        load_instance = True
        transient = True

    post = fields.Nested('PostSchema')
    
    Promotion.end_date = JADateTime(attribute='end_date')

    @post_dump
    def flatten_post(self, data, **kwargs):
        post_data = data.pop('post')
        data = {**data, **post_data}
        return data


class GasTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GasType
        include_relationships = True
        load_instance = True
        transient = True


class GasSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Gas
        include_relationships = True
        load_instance = True
        transient = True

    price = fields.Decimal(as_string=True)
    gas_type = fields.Nested('GasTypeSchema')
    gas_post = fields.Nested('GasPriceSuggestionSchema', exclude=(
        'gases', 'post.gas_station.reviews', 'post.gas_station.promotions',
        'post.gas_station.image', 'post.gas_station.amenities',
        'post.gas_station.gas_price_suggestions',
        'post.gas_station.current_best_price',
        'post.gas_station.old_best_price', 'post.creator',
        'post.upvoters', 'post.downvoters', 'post.gas_station.manager'))


class GasPriceSuggestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GasPriceSuggestion
        include_relationships = True
        load_instance = True
        transient = True

    post = fields.Nested('PostSchema')
    gases = fields.Nested('GasSchema', many=True, exclude=('gas_post',))

    @post_dump
    def flatten_post(self, data, **kwargs):
        post_data = data.pop('post', dict())
        data = {**data, **post_data}
        return data


class AmenityTagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AmenityTag
        include_relationships = True
        load_instance = True
        transient = True

    post = fields.Nested('PostSchema')
    amenity_type = fields.Nested('AmenityTypeSchema')

    @post_dump
    def flatten_post(self, data, **kwargs):
        post_data = data.pop('post')
        data = {**data, **post_data}
        return data


class PostTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PostType
        include_fk = True
        include_relationships = True
        load_instance = True
        transient = True
        exclude = ('posts',)


class UserTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserType
        #include_fk = True
        include_relationships = True
        load_instance = True
        transient = True
        exclude = ('users',)

    allowed_post_types = fields.Nested(
        'PostTypeSchema', many=True, exclude=('allowed_user_types', 'posts'))


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True
        include_relationships = True
        load_instance = True
        transient = True
        exclude = ('downvoters','upvoters')

    post_type = fields.Nested(
        'PostTypeSchema', exclude=('allowed_user_types',))
    creator = fields.Nested('UserSchema', exclude=('managed_gasstations', 'firstname',
                            'lastname', 'created_at', 'id', 'email', 'user_type.allowed_post_types'))
    upvote_count = fields.Integer(attribute='upvote_count', dump_only=True)
    downvote_count = fields.Integer(attribute='downvote_count', dump_only=True)
    net_votes = fields.Integer(attribute='net_votes', dump_only=True)
    gas_station = fields.Nested('GasStationSchema')
    
    last_edited = JADateTime()
    created_at = JADateTime()
    deleted_at = JADateTime()


class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        include_fk = True
        include_relationships = True
        load_instance = True
        transient = True
        exclude = ('id', 'post_id')

    post = fields.Nested('PostSchema')

    @post_dump
    def flatten_post(self, data, **kwargs):
        post_data = data.pop('post', dict())
        data = {**data, **post_data}
        return data


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        #include_fk = True
        include_relationships = True
        load_instance = True
        transient = True
        exclude = ("_password", 'posts', 'upvoted_posts', 'downvoted_posts')

    user_type = fields.Nested('UserTypeSchema')
    managed_gasstations = fields.Nested('GasStationSchema', many=True)

    post_count = fields.Int(strict=True, dump_only=True, dump_default=0)
    reputation = fields.Int(strict=True, dump_only=True, dump_default=0)
    level = fields.Str(dump_only=True, dump_default='None')

    @post_load
    def load_user(self, data, **kwargs):
        passwd = data.pop('_password', None)
        if passwd:
            data['password'] = passwd

        varnames = User.__init__.__code__.co_varnames

        moddata = dict()
        for key, value in data.items():
            if key in varnames:
                moddata[key] = value

        return moddata


class GasStationSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = GasStation
        include_relationships = True
        load_instance = True
        transient = True
        exclude = ('all_posts',)

    reviews = fields.Nested(ReviewSchema, many=True,
                            dump_only=True, exclude=('post.gas_station',))

    promotions = fields.Nested(
        PromotionSchema, many=True, dump_only=True, exclude=('post.gas_station',))

    amenities = fields.Nested(
        AmenityTagSchema, many=True, dump_only=True, exclude=('post.gas_station',))

    gas_price_suggestions = fields.Nested(
        GasPriceSuggestionSchema, many=True, dump_only=True, exclude=('post.gas_station',))

    avg_rating = fields.Float(dump_only=True)

    verified = fields.Bool(dump_only=True)

    manager = fields.Nested(UserSchema, exclude=('managed_gasstations',))

    current_best_price = fields.Nested(
        GasSchema,many=True, dump_only=True)

    old_best_price = fields.Nested(
        GasSchema,many=True, dump_only=True)
