from config import ma
from model.gasstation import *
from model.users import *
from model.posts import *

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post


class RatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        include_fk = True

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_fk = True
        
class PostsSchema(ma.SQLAlchemySchema):
    comments = None