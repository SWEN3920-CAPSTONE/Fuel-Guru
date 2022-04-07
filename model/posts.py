from datetime import datetime
from sqlalchemy.schema import MetaData
from config import db


# Many-to-many join tables

upvoted_posts = db.Table('upvoted_posts',
                        db.Column('posts',db.ForeignKey('posts.id'), primary_key=True), 
                        db.Column('users', db.ForeignKey('users.id'), primary_key=True))

downvoted_posts = db.Table('downvoted_posts',
                        db.Column('posts',db.ForeignKey('posts.id'), primary_key=True), 
                        db.Column('users', db.ForeignKey('users.id'), primary_key=True))


# Regular tables

class Post(db.Model):
    __tablename__ = 'posts'
    
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    deleted_at = db.Column(
        db.DateTime,
        nullable=True
    )
    
    created_at = db.Column(
        db.DateTime,
        default = datetime.utcnow,
        nullable=False
    )
    
    last_edited = db.Column(
        db.DateTime,
        default = datetime.utcnow,
        nullable = False
    )
    
    gas_station_id = db.Column(
        db.Integer,
        db.ForeignKey('gas_stations.id'),
        nullable=False
    )
    
    post_type_id = db.Column(
        db.Integer,
        db.ForeignKey('post_types.id'),
        nullable=False
    )
    
    upvoters = db.relationship('User', secondary= upvoted_posts, backref='upvoted_posts')
    
    downvoters = db.relationship('User', secondary = downvoted_posts, backref='downvoted_posts')
    
    def __init__(self,deleted_at, created_at, last_edited, gas_station_id, post_type_id) -> None:
        self.deleted_at = deleted_at
        self.created_at = created_at
        self.last_edited = last_edited
        self.gas_station_id = gas_station_id
        self.post_type_id = post_type_id
    
    
class PostType(db.Model):
    __tablename__ = 'post_types'
    
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    post_type_name = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    
    is_votable = db.Column(
        db.Boolean,
        nullable=False
    )
    
    def __init__(self, post_type_name,is_votable) -> None:
        self.post_type_name = post_type_name
        self.is_votable = is_votable
        

# Additional Post content

class AmenityType(db.Model):
    __tablename__ = 'amenity_types'
    
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    amenity_name = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    
    def __init__(self,amenity_name) -> None:
        self.amenity_name = amenity_name
        
        
class GasType(db.Model):
    __tablename__ = 'gas_types'
    
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    gas_type_name = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    
    def __init__(self, gas_type_name) -> None:
        self.gas_type_name = gas_type_name
    
    
class Gas(db.Model):
    __tablename__ = 'gases'
    
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    price = db.Column(
        db.Numeric,
        nullable=False
    )
    
    gas_type_id = db.Column(
        db.Integer,
        db.ForeignKey('gas_types.id'),
        nullable=False
    )
    
    gas_post_id = db.Column(
        db.Integer,
        db.ForeignKey('gas_price_suggestions.id'),
        nullable=False
    )
    
    def __init__(self, price, gas_type_id, gas_post_id) -> None:
        self.gas_post_id = gas_post_id
        self.gas_type_id = gas_type_id
        self.price = price

    
# Post Types

class GasPriceSuggestion(db.Model):
    __tablename__ = 'gas_price_suggestions'
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    last_edited = db.Column(
        db.DateTime,
        nullable=False
    )
    
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id')
    )
    
    gases = db.relationship('Gas', backref='gas_post')
    
    def __init__(self, last_edited, post_id) -> None:
        self.last_edited = last_edited
        self.post_id = post_id
    
    
class AmenityTag(db.Model):
    __tablename__ = 'amenity_tags'
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    last_edited = db.Column(
        db.DateTime,
        nullable=False
    )
    
    amenity_type_id = db.Column(
        db.Integer,
        db.ForeignKey('amenity_types.id'),
        nullable=False
    )
    
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id')
    )
    
    def __init__(self, last_edited, amenity_type_id, post_id) -> None:
        self.last_edited = last_edited
        self.amenity_type_id = amenity_type_id
        self.post_id = post_id
        

class Promotion(db.Model):
    __tablename__ = 'promotions'
    
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    last_edited = db.Column(
        db.DateTime,
        nullable=False
    )
    
    start_date = db.Column(
        db.DateTime,
        nullable=False
    )
    
    end_date = db.Column(
        db.DateTime,
        nullable=False
    )
    
    image = db.Column(
        db.String(255),
        nullable=True
    )
    
    desc = db.Column(
        db.String(255),
        nullable=True
    )
    
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id')
    )
    
    def __init__(self, last_edited, start_date, end_date, image,desc,post_id) -> None:
        self.last_edited = last_edited
        self.start_date = start_date
        self.end_date = end_date
        self.image = image
        self.desc = desc
        self.post_id = post_id
        
    
class Rating(db.Model):
    __tablename__ = 'ratings'
    
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    last_edited = db.Column(
        db.DateTime,
        nullable=False
    )
    
    rating_val = db.Column(
        db.Integer,
        nullable=False
    )
    
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id')
    )
    
    def __init__(self, last_edited, rating_val, post_id) -> None:
        self.last_edited = last_edited
        self.rating_val =rating_val
        self.post_id = post_id
    
class Comment(db.Model):
    __tablename__ = 'comments'
    
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    last_edited = db.Column(
        db.DateTime,
        nullable=False
    )
    
    body = db.Column(
        db.String(500),
        nullable=True
    )
    
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id')
    )
    
    def __init__(self, last_edited, body, post_id) -> None:
        self.last_edited = last_edited
        self.body = body
        self.post_id = post_id
    
    
