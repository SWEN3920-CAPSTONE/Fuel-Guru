from config import ma
from model.gasstation import *
from model.users import *
from model.posts import *
from marshmallow import fields, post_load

class PromotionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Promotion

class GasPriceSuggestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GasPriceSuggestion
        
class AmenityTagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AmenityTag
        
class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        
class RatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        
class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_fk = True
        include_relationships = True
        load_instance = True
        transient = True
    
class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        pass
    
    comments = fields.Nested(CommentSchema, many=True)
    

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        include_relationships = True
        load_instance = True
        transient = True
        exclude = ("_password",)
    
    password = fields.String(attribute='_password')
    
    @post_load
    def load_user(self, data, **kwargs):
        data['password'] = data.pop('_password')
        varnames = User.__init__.__code__.co_varnames
        
        for key in data:
            if not key in varnames:
                data.pop(key)
        
        return data
        