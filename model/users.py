from functools import reduce
from config import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method


class User(db.Model):
    """
    Represents a registered user in Fuel Guru.
    """

    __tablename__ = 'users'

    # Columns

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    """The unique identifier and table primary key"""

    username = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    _password = db.Column(
        'password',
        db.String(255),
        nullable=False
    )
    """The user's password (hashed)"""

    firstname = db.Column(
        db.String(255),
        nullable=False
    )

    lastname = db.Column(
        db.String(255),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    user_type_id = db.Column(
        db.Integer,
        db.ForeignKey('user_types.id'),
        nullable=False
    )
    """A ForeignKey to the UserType model"""

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    """The UTC date and time at which the user was created"""

    deleted_at = db.Column(
        db.DateTime,
        nullable=True
    )
    """The UTC date and time at which the user was deleted"""

    posts = db.relationship('Post', backref='creator')
    """SQLAlchemy relationship to get all posts created by a user"""

    def __init__(self, username, email, firstname, lastname, password, user_type, deleted_at=None, id=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = created_at or datetime.utcnow()
        self.firstname = firstname
        self.lastname = lastname
        self.deleted_at = deleted_at
        self.user_type = user_type
        self.password = password  # this will be hashed by password.setter

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        """
        Sets the password for a user to a hashed password

        Args:
            password (str):
                The plain text password to be hashed

        Returns:
            None
        """

        self._password = generate_password_hash(
            password, method='pbkdf2:sha256')  # store password hashes, never the plain text password for security reasons

    @hybrid_method
    def check_password(self, password):
        """
        Checks the password argument against this User's password

        Args:
            password (str):
                The plain text password to be checked

        Returns:
            bool: True if the password matches the hash, otherwise False
        """

        return check_password_hash(self._password, password)

    @hybrid_property
    def reputation(self):
        return reduce(lambda a, b: a + b.upvotes, self.posts, 0) - reduce(lambda a, b: a + b.downvotes, self.posts, 0) 

    @hybrid_property
    def level(self):
        if self.reputation == 0:
            return 'None'  # we never actually fleshed out what the ranges would be for the levels
        return 'Guru' #temp

    @hybrid_property
    def post_count(self):
        return len(self.posts)

    def __repr__(self) -> str:
        return f'<{self.id}, {self.username}> {self.firstname} {self.lastname}'


post_types_for_user_types = db.Table('post_types_for_user_types',
                                     db.Column('post_types', db.ForeignKey(
                                         'post_types.id'), primary_key=True),
                                     db.Column('user_types', db.ForeignKey('user_types.id'), primary_key=True))
"""
Represents a many-to-many join table between PostType and UserType where 
one PostType can be posted by many UserTypes and one UserType can post 
many PostTypes
"""


class UserType(db.Model):
    """
    Represents the different user types in Fuel Guru

    Currently there are:
    - Normal Users
    - Gas Station Managers
    - System Users
    """

    __tablename__ = 'user_types'

    # Columns

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_type_name = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    can_vote = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    users = db.relationship('User', backref='user_type')
    """SQLAlchemy relationship to get all users of a specifc type"""

    allowed_post_types = db.relationship(
        'PostType', secondary=post_types_for_user_types, backref='allowed_user_types', cascade='all, delete')
    """SQLAlchemy relationship to get the post types this user type is allowed to make"""

    def __init__(self, user_type_name, is_admin, can_vote, id=None) -> None:
        self.user_type_name = user_type_name
        self.is_admin = is_admin
        self.can_vote = can_vote
        self.id = id

    def __repr__(self):
        return f'{self.user_type_name}'
