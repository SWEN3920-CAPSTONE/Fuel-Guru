from config import ma
from model.gasstation import *
from model.users import *
from model.posts import *
from marshmallow import fields, post_dump, post_load


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
        
    gas_type = fields.Nested('GasTypeSchema')

class GasPriceSuggestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GasPriceSuggestion
        include_relationships = True
        load_instance = True
        transient = True
        
    post = fields.Nested('PostSchema')
    gases = fields.Nested('GasSchema')

    @post_dump
    def flatten_post(self, data, **kwargs):
        post_data = data.pop('post')
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


class UserTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserType
        include_fk = True
        include_relationships = True
        load_instance = True
        transient = True


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        #include_fk = True
        include_relationships = True
        load_instance = True
        transient = True
        exclude = ('gas_station','downvoters','upvoters')

    post_type = fields.Nested('PostTypeSchema', exclude=('posts',))
    creator = fields.Nested('UserSchema', exclude=(
        'posts', 'managed_gasstations', 'downvoted_posts', 'upvoted_posts', 'firstname', 'lastname', 'user_type_id', 'user_type','created_at','id','email'))
    upvote_count = fields.Integer(attribute='upvote_count')
    downvote_count = fields.Integer(attribute='downvote_count')


class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        include_fk = True
        include_relationships = True
        load_instance = True
        transient = True
        exclude=('id','comment', 'rating','post_id')

    post = fields.Nested('PostSchema')
    body = fields.Pluck('CommentSchema', 'body', attribute='comment')
    rating_val = fields.Pluck('RatingSchema', 'rating_val', attribute='rating')

    @post_dump
    def flatten_post(self, data, **kwargs):
        post_data = data.pop('post')
        data = {**data, **post_data}
        return data

class RatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        include_fk = True
        include_relationships = True
        load_instance = True
        transient = True
        exclude = ('review', 'review_id', 'id')

    #post = fields.Pluck('ReviewSchema', 'post', attribute='review')

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_fk = True
        include_relationships = True
        load_instance = True
        transient = True
        exclude = ('review', 'review_id','id')

    #post = fields.Pluck('ReviewSchema', 'post', attribute='review')


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        include_relationships = True
        load_instance = True
        transient = True
        exclude = ("_password",)

    user_type = fields.Nested('UserTypeSchema', exclude=('users',))

    @post_load
    def load_user(self, data, **kwargs):
        data['password'] = data.pop('_password')
        varnames = User.__init__.__code__.co_varnames

        for key in data:
            if not key in varnames:
                data.pop(key)

        return data

class GasStationSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = GasStation
        include_relationships = True
        load_instance = True
        transient = True