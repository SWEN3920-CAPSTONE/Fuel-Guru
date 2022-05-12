from datetime import datetime
from sqlalchemy import ForeignKeyConstraint
from config import db
from sqlalchemy.ext.hybrid import hybrid_property


# Many-to-many join tables

upvoted_posts = db.Table('upvoted_posts',
                         db.Column('posts', db.ForeignKey(
                             'posts.id'), primary_key=True),
                         db.Column('users', db.ForeignKey('users.id'), primary_key=True))
"""
Represents a many-to-many join table between Post and User where
one Post can be upvoted by many Users and one User can upvote many Posts
"""

downvoted_posts = db.Table('downvoted_posts',
                           db.Column('posts', db.ForeignKey(
                               'posts.id'), primary_key=True),
                           db.Column('users', db.ForeignKey('users.id'), primary_key=True))
"""
Represents a many-to-many join table between Post and User where
one Post can be downvoted by many Users and one User can downvote many Posts
"""

# Regular tables

class Post(db.Model):
    """
    Represents the Posts that can be made in the Fuel Guru 
    system and stores the information common to all post types.
    """

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
    """
    The UTC date and time that this post was deleted if it 
    has been deleted, otherwise this field will be null.
    """

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    """The UTC date and time that this post was created"""

    last_edited = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    """
    The UTC date and time that this post was last edited.
    This will be the same as created_at for a Post that has never been edited.
    """

    gas_station_id = db.Column(
        db.Integer,
        db.ForeignKey('gas_stations.id'),
        nullable=False
    )
    """
    A ForeignKey to the GasStation Model representing the Gas Station
    this post was made on.
    """

    post_type_id = db.Column(
        db.Integer,
        db.ForeignKey('post_types.id'),
        nullable=False
    )
    """
    A ForeignKey to the PostType Model representing the type of post 
    this Post is.
    """

    creator_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    """
    A ForeignKey to the User Model representing the user that created this post
    """

    upvoters = db.relationship(
        'User', secondary=upvoted_posts, backref='upvoted_posts', cascade='all, delete')
    """SQLAlchemy relationship to get all the Users who upvoted this Post"""

    downvoters = db.relationship(
        'User', secondary=downvoted_posts, backref='downvoted_posts', cascade='all, delete')
    """SQLAlchemy relationship to get all the Users who downvoted this Post"""

    post_type = db.relationship('PostType', backref='posts')

    def __init__(self, gas_station, post_type, creator, deleted_at=None) -> None:
        self.creator = creator
        self.deleted_at = deleted_at
        self.created_at = datetime.utcnow()
        self.last_edited = self.created_at
        self.gas_station = gas_station
        self.post_type = post_type

    def __repr__(self) -> str:
        return f'Post {self.id} - {self.post_type}'

    @hybrid_property
    def upvote_count(self):
        return len(self.upvoters)

    @hybrid_property
    def downvote_count(self):
        return len(self.downvoters)


class PostType(db.Model):
    """
    Represents the types of Posts allowed in Fuel Guru.

    Currently there are:
    - Promotion
    - Comment
    - Rating
    - Review (Rating + Comment)
    - Gas Price Suggestion
    - Amenity Tag
    """

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
    """The name of this PostType"""

    is_votable = db.Column(
        db.Boolean,
        nullable=False
    )
    """Whether this PostType can be upvoted or downvoted by Users"""

    def __init__(self, post_type_name, is_votable, id=None) -> None:
        self.post_type_name = post_type_name
        self.is_votable = is_votable
        self.id = id

    def __repr__(self) -> str:
        return f'<{self.id}: {self.post_type_name}>'


# Additional Post content

class AmenityType(db.Model):
    """
    Represents the types of amenities that Users can post in Fuel Guru
    """

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

    def __init__(self, amenity_name) -> None:
        self.amenity_name = amenity_name

    def __repr__(self) -> str:
        return f'{self.amenity_name}'


class GasType(db.Model):
    """
    Represents the types of Gas that Users can post in a GasPriceSuggestion
    in Fuel Guru
    """

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

    def __repr__(self) -> str:
        return f'{self.gas_type_name}'


class Gas(db.Model):
    """
    Represents the Gas that Users have Posted in GasPriceSuggestions
    in Fuel Guru
    """

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
    """The price for this Gas the User saw"""

    gas_type_id = db.Column(
        db.Integer,
        db.ForeignKey('gas_types.id'),
        nullable=False
    )
    """A ForeignKey to the GasType Model representing the type of gas 
    this Gas is"""

    gas_post_id = db.Column(
        db.Integer,
        db.ForeignKey('gas_price_suggestions.id'),
        nullable=False
    )
    """
    A ForeignKey to the GasPriceSuggestion Model representing the specific
    GasPriceSuggestion Post that this Gas was in
    """

    gas_type = db.relationship('GasType')

    def __init__(self, price, gas_type, gas_post) -> None:
        self.gas_post = gas_post
        self.gas_type = gas_type
        self.price = price


# Post Types

class GasPriceSuggestion(db.Model):
    """
    Represents the information related to GasPriceSuggestions 
    that the other post types do not have.
    """

    __tablename__ = 'gas_price_suggestions'

    # Columns

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,  # required when the primary key is composite
        unique=True
    )

    last_edited = db.Column(
        db.DateTime,
        nullable=False
    )
    """
    The UTC date and time that this GasPriceSuggestion was last edited. 
    If this GasPriceSuggestion is the most recent edit, this timestamp
    will be the same as the last_edited field for the corresponding Post object.
    """

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True
    )
    """A ForeignKey to the Post Model linking this GasPriceSuggestion to information related to it"""

    gases = db.relationship('Gas', backref='gas_post')
    """SQLAlchemy relationship to get all the gases posted with this 
    gas price suggestion"""

    post = db.relationship(
        'Post', primaryjoin='and_(GasPriceSuggestion.post_id == Post.id, Post.last_edited == GasPriceSuggestion.last_edited)')

    def __init__(self, post, edit=False) -> None:
        if edit:
            post.last_edited = datetime.utcnow()
        self.last_edited = post.last_edited
        self.post = post


class AmenityTag(db.Model):
    """
    Represents the information related to Amenity Tags
    that the other post types do not have.
    """

    __tablename__ = 'amenity_tags'
    # Columns

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,  # required when the primary key is composite
        unique=True
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
        db.ForeignKey('posts.id'),
        primary_key=True
    )

    amenity_type = db.relationship('AmenityType')

    post = db.relationship(
        'Post', primaryjoin='and_(AmenityTag.post_id == Post.id, Post.last_edited == AmenityTag.last_edited)')

    def __init__(self, amenity_type, post, edit=False) -> None:
        if edit:
            post.last_edited = datetime.utcnow()
        self.last_edited = post.last_edited
        self.amenity_type = amenity_type
        self.post = post


class Promotion(db.Model):
    """
    Represents the information related to Promotions 
    that the other post types do not have.
    """

    __tablename__ = 'promotions'

    # Columns

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,  # required when the primary key is composite
        unique=True
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
        db.LargeBinary,
        nullable=True
    )

    desc = db.Column(
        db.String(255),
        nullable=True
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True
    )

    post = db.relationship(
        'Post', primaryjoin='and_(Promotion.post_id == Post.id, Post.last_edited == Promotion.last_edited)')

    def __init__(self, start_date, end_date, image, desc, post, edit=False) -> None:
        if edit:
            post.last_edited = datetime.utcnow()
        self.last_edited = post.last_edited
        self.start_date = start_date
        self.end_date = end_date
        self.image = image
        self.desc = desc
        self.post = post


class Review(db.Model):
    """
    A representation of a special case in the system where a 
    comment and a review together make a review. 

    However, to simplify the serialization process on the api end, 
    all comments and ratings will be treated as reviews that contain 
    a single comment or a single rating or both a rating and a comment. 
    For those cases, the post type in the Post table will still 
    indicate Comment, Rating or Review respectively.
    """

    __tablename__ = 'reviews'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,  # required when the primary key is composite
        unique=True
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True,
        unique=True
    )

    last_edited = db.Column(
        db.DateTime,
        nullable=False
    )

    comment = db.relationship('Comment', backref='review', uselist=False,
                              primaryjoin='and_(Comment.review_id == Review.id, Review.post_id == Comment.post_id, Comment.last_edited == Review.last_edited)')
    """Could be None if rating is not None"""

    rating = db.relationship('Rating', backref='review', uselist=False,
                             primaryjoin='and_(Rating.review_id == Review.id, Review.post_id == Rating.post_id, Rating.last_edited == Review.last_edited)')
    """Could be None if comment is not None"""

    post = db.relationship(
        'Post', primaryjoin='and_(Review.post_id == Post.id, Post.last_edited == Review.last_edited)')

    def __init__(self, post):
        self.post = post
        self.last_edited = post.last_edited


class Rating(db.Model):
    """
    Represents the information related to Ratings 
    that the other post types do not have.
    """

    __tablename__ = 'ratings'

    # Columns

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,  # required when the primary key is composite
        unique=True
    )

    rating_val = db.Column(
        db.Integer,
        nullable=False
    )

    last_edited = db.Column(
        db.DateTime,
        nullable=False
    )

    review_id = db.Column(
        db.Integer,
        primary_key=True
    )

    post_id = db.Column(
        db.Integer,
        primary_key=True
    )

    __table_args__ = (ForeignKeyConstraint(
        [review_id, post_id], [Review.id, Review.post_id]),)

    def __init__(self, rating_val, review, edit=False) -> None:
        if edit:
            tnow = datetime.utcnow()
            review.last_edited = tnow
            review.post.last_edited = tnow
        self.last_edited = review.last_edited
        self.rating_val = rating_val
        self.review = review


class Comment(db.Model):
    """
    Represents the information related to Comment 
    that the other post types do not have.
    """

    __tablename__ = 'comments'

    # Columns

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,  # required when the primary key is composite
        unique=True
    )

    body = db.Column(
        db.String(500),
        nullable=True
    )

    last_edited = db.Column(
        db.DateTime,
        nullable=False
    )

    review_id = db.Column(
        db.Integer,
        primary_key=True
    )

    post_id = db.Column(
        db.Integer,
        primary_key=True
    )

    __table_args__ = (ForeignKeyConstraint([review_id, post_id], [
                      Review.id, Review.post_id]),)  # composite ForeignKey

    def __init__(self, body, review, edit=False) -> None:
        if edit:
            tnow = datetime.utcnow()
            review.last_edited = tnow
            review.post.last_edited = tnow
        self.last_edited = review.last_edited
        self.body = body
        self.review = review
