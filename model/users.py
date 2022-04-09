from config import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

class User(db.Model): 
    """
    Represents a registered user in Fuel Guru.
    """
    
    __tablename__ = 'users'
    
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    """The unique identifier and table primary key"""
    
    username = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    password = db.Column(
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
        default = datetime.utcnow,
        nullable=False
    )
    """The UTC date and time at which the user was created"""
    
    def __init__(self, username, email, firstname, lastname, password, user_type_id,created_at=datetime.utcnow()):
        self.username = username
        self.email = email
        self.created_at = created_at
        self.firstname = firstname
        self.lastname = lastname
        self.user_type_id = user_type_id
        self.password = generate_password_hash(
            password, method='pbkdf2:sha256') # store password hashes, never the plain text password for security reasons

    def check_password(self, password):
        """
        Checks the password argument against this User's password
        
        Args:
            password (str):
                The plain text password to be checked
                
        Returns:
            bool: True if the password matches the hash, otherwise False
        """
        
        return check_password_hash(self.password, password)


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
        primary_key = True
    )
    
    user_type_name = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    
    users = db.relationship('User')
    """SQLAlchemy relationship to get all users of a specifc type"""
    
    def __init__(self, user_type_name) -> None:
        self.user_type_name = user_type_name

